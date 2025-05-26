from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    EventViewSet, LocationViewSet, OrganizerViewSet, DepartmentViewSet,
    TagViewSet, AttendeeViewSet, AttachmentViewSet, RecurringPatternViewSet,
    EventChangeLogViewSet
)


# Optional API versioning prefix
urlpatterns = [
    path('events/', EventViewSet.as_view()),
    path('locations/', LocationViewSet.as_view()),
    path('organizers/', OrganizerViewSet.as_view()),
    path('departments/', DepartmentViewSet.as_view()),
    path('tags/', TagViewSet.as_view()),
    path('attendees/', AttendeeViewSet.as_view()),
    path('attachments/', AttachmentViewSet.as_view()),
    path('recurring-patterns/', RecurringPatternViewSet.as_view()),
    path('event-changes/', EventChangeLogViewSet.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)