"""
Views for the Calendar/Events Microservice
"""
import datetime

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from .models import (
    Event, Location, Organizer, Department, Tag,
    Attendee, Attachment, RecurringPattern, EventChangeLog
)
from .serializers import (
    EventListSerializer, EventDetailSerializer, LocationSerializer,
    OrganizerSerializer, DepartmentSerializer, TagSerializer,
    AttendeeSerializer, AttachmentSerializer, RecurringPatternSerializer,
    EventChangeLogSerializer
)

#https://www.django-rest-framework.org/api-guide/viewsets/
#viewset provides .list()& .create()
#ModelViewSet provides all CRUD operations
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_accessible', 'city', 'state']
    search_fields = ['name', 'address']


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class OrganizerViewSet(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department']
    search_fields = ['name', 'email']


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_public', 'is_featured', 'location', 'organizer', 'tags', 'departments']
    search_fields = ['title', 'description']
    ordering_fields = ['start_time', 'end_time', 'created_at', 'updated_at']
    ordering = ['start_time']

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        return EventDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(start_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_time__lte=end_date)

        # Filter for upcoming events
        upcoming = self.request.query_params.get('upcoming')
        if upcoming == 'true':
            now = timezone.now()
            queryset = queryset.filter(start_time__gte=now)

        # Filter by registration requirement
        registration = self.request.query_params.get('registration_required')
        if registration is not None:
            registration_bool = registration.lower() == 'true'
            queryset = queryset.filter(registration_required=registration_bool)

        return queryset

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        event = self.get_object()
        event.status = 'cancelled'
        event.notification_sent = False  # Trigger notification
        event.save()

        # Create change log entry
        EventChangeLog.objects.create(
            event=event,
            field_name='status',
            old_value='scheduled',
            new_value='cancelled'
        )

        return Response({'status': 'Event cancelled'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def this_week(self, request):
        today = timezone.now().date()
        end_of_week = today + datetime.timedelta(days=6)

        queryset = self.get_queryset().filter(
            start_time__date__gte=today,
            start_time__date__lte=end_of_week
        )

        serializer = EventListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        queryset = self.get_queryset().filter(is_featured=True, start_time__gte=timezone.now())
        serializer = EventListSerializer(queryset, many=True)
        return Response(serializer.data)


class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['event', 'attended', 'notification_preference']
    search_fields = ['name', 'email']

    @action(detail=False, methods=['get'])
    def my_events(self, request):
        # Assuming user email is available in request
        user_email = request.user.email
        attendees = self.get_queryset().filter(email=user_email)
        event_ids = attendees.values_list('event_id', flat=True)
        events = Event.objects.filter(id__in=event_ids)

        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']


class RecurringPatternViewSet(viewsets.ModelViewSet):
    queryset = RecurringPattern.objects.all()
    serializer_class = RecurringPatternSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'frequency']


class EventChangeLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view for notification service to consume"""
    queryset = EventChangeLog.objects.filter(processed_by_notification_service=False)
    serializer_class = EventChangeLogSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def mark_processed(self, request, pk=None):
        change_log = self.get_object()
        change_log.processed_by_notification_service = True
        change_log.save()
        return Response({'status': 'Change log marked as processed'})

    @action(detail=False, methods=['post'])
    def mark_all_processed(self, request):
        count = self.get_queryset().update(processed_by_notification_service=True)
        return Response({'status': f'{count} change logs marked as processed'})