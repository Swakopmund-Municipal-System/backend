"""
URL configuration for admin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL Configuration for the Calendar/Events Microservice
"""
from django.urls import path, include
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

# Optional API versioning prefix
api_urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('api/event/', include(api_urlpatterns)),
]