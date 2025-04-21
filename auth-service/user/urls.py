from django.urls import path

# rest framework imports
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# Knox imports
from knox import views as knox_views

# app imports
from .views import CheckUserPermission, LoginView, CreateUserView, ValidateUserTokenView

urlpatterns = [
    path('sign-up/', CreateUserView.as_view(), name='create_user'),
    path('check-user-permission/', CheckUserPermission.as_view(), name='check_user_permission'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('validate', ValidateUserTokenView.as_view(), name='validate_token'),
]

urlpatterns = format_suffix_patterns(urlpatterns)