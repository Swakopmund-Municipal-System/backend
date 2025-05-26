from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from .views import (
    EventViewSet, LocationViewSet, OrganizerViewSet, DepartmentViewSet,
    TagViewSet, AttendeeViewSet, AttachmentViewSet, RecurringPatternViewSet,
    EventChangeLogViewSet
)

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'organizers', OrganizerViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'tags', TagViewSet)
router.register(r'attendees', AttendeeViewSet)
router.register(r'attachments', AttachmentViewSet)
router.register(r'recurring-patterns', RecurringPatternViewSet)
router.register(r'event-changes', EventChangeLogViewSet)

urlpatterns = router.urls