from django.urls import path
from eco_dev import views

urlpatterns = [
        path('businesses/', views.businesses_public),
        path('businesses/admin/', views.get_business_reg_requests),
        path('businesses/admin/<id>', views.reg_request_detail),
        # path('tourism/attractions/', views.get_tourist_attractions),
        # path('tourism/events/', views.get_upcoming_events),
]
