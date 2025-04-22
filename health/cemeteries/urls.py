from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import CemeteryPlotView

urlpatterns = [
    path('cemetery/', CemeteryPlotView.as_view(), name='cemetery-plots-list'),
    path('cemetery/<str:plot_id>/', CemeteryPlotView.as_view(), name='cemetery-plot-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)