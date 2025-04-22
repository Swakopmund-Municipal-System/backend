from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import EnvironmentView


urlpatterns = [
    path('environment/', EnvironmentView.as_view(), name='environment-list'),
    path('environment/<uuid:report_id>/', EnvironmentView.as_view(), name='environment-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)