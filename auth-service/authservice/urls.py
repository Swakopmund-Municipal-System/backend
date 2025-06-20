"""
URL configuration for authservice project.

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('api/auth/admin/', admin.site.urls),
    path('api/auth/application/', include('application.urls')),
    path('api/auth/user/', include('user.urls')),
    path('api/authenticate/', include('knox.urls')),
    path('api/auth/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/auth/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/auth/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
