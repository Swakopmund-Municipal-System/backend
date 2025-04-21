from django.urls import path

# rest framework imports
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# app imports
from .views import ApplicationListView, CheckApplicationPermissionView, ValidateAPIKeyView

urlpatterns = [
    path('', ApplicationListView.as_view()),
    path('check_application_permission/', CheckApplicationPermissionView.as_view()),
    path('validate', ValidateAPIKeyView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)