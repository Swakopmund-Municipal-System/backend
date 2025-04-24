from poi import views
from django.urls import path

urlpatterns = [
    # public
    path('places/', views.place_list),
    path('places/<id>', views.place_details),
    # admin
    # create new app for admin actionsls
    path('admin/places', views.admin_create_poi),
    path('admin/places/<id>', views.admin_poi_detail)
]