from django.urls import path
from .views import get_locations_weather, get_tide_forecast

urlpatterns = [
    path('weather/', get_locations_weather),
    path('weather/tide/', get_tide_forecast)
]