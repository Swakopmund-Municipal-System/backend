from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import ComplaintView, ComplaintImageView


urlpatterns = [
    path('complaints/', ComplaintView.as_view(), name='complaints-list'),
    path('complaints/<uuid:complaint_id>/', ComplaintView.as_view(), name='complaint-detail'),
    path('complaints/<uuid:complaint_id>/images/', ComplaintImageView.as_view(), name='complaint-images'),
    path('complaints/<uuid:complaint_id>/images/<str:image_id>/', ComplaintImageView.as_view(), name='complaint-image-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)