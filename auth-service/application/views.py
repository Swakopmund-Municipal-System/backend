from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User
from django_filters import rest_framework
import secrets

from rest_framework.permissions import IsAuthenticated, AllowAny
# Rest Framework Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

# App Imports
from .models import Application, Resource, SubResource, ApplicationResourcePermission
from .serializers import ApplicationSerializer, ResourceSerializer, SubResourceSerializer, ApplicationResourcePermissionSerializer

from django.utils import timezone
from datetime import timedelta
import uuid
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError
from datetime import datetime

# Views
class ApplicationListView(APIView):
    """
    List all applications or create a new application.
    """
    
    def get(self, request):
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()
            return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CheckApplicationPermissionView(APIView):
    """
    Verify if the application has permission to access the resource.
    """
    
    permission_classes = [AllowAny]
    
    # Map HTTP methods to required permission levels
    METHOD_TO_PERMISSION = {
        'GET': 'read',
        'POST': 'write',
        'PUT': 'write',
        'PATCH': 'write',
        'DELETE': 'admin',
    }
    
    def post(self, request):
        api_key = request.headers.get('X-API-KEY')
        
        try:
            application = Application.objects.get(api_key=api_key, is_active=True)
            if application.api_key_expiration < timezone.now():
                return Response({"error": "API Key has expired"}, status=status.HTTP_403_FORBIDDEN)
            
        except Application.DoesNotExist:
            return Response({"error": "Invalid API Key"}, status=status.HTTP_403_FORBIDDEN)
        
        requested_resource = request.headers.get('x-resource')
        http_method = request.headers.get('x-method', 'GET').upper()  # Default to GET if not specified
        
        # Get the required permission based on HTTP method
        required_permission = self.METHOD_TO_PERMISSION.get(http_method, 'read')
        
        try:
            app_permission = ApplicationResourcePermission.objects.get(
                application=application,
                resource__name=requested_resource
            )
            
            # Check if the application has the required permission
            permission_hierarchy = ['read', 'write', 'admin']
            
            # Get the highest permission the application has for this resource
            highest_app_permission = max(
                app_permission.permission,
                key=lambda p: permission_hierarchy.index(p)
            )
            
            # Check if the highest permission meets the requirement
            if permission_hierarchy.index(highest_app_permission) < permission_hierarchy.index(required_permission):
                return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            
        except ApplicationResourcePermission.DoesNotExist:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            "status": "authorised",
            "application": application.name,
            "resource": requested_resource,
            "permission": highest_app_permission,
            }, status=status.HTTP_200_OK)
        
        
class ValidateAPIKeyView(APIView):
    """
    Validate the API key and check its expiration.
    """
    
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def post(self, request):
        api_key = request.headers.get('X-API-KEY')
        
        if not api_key:
            return Response({"error": "Invalid API key"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            application = Application.objects.get(api_key=api_key, is_active=True)
            
            if application.api_key_expiration and application.api_key_expiration < timezone.now():
                return Response({"error": "API Key has expired"}, status=status.HTTP_403_FORBIDDEN)
            
            app_info = {
                'id': application.id,
                "name": application.name,
            }
            
            return Response({
                "status": "valid",
                "application": app_info,
            }, status=status.HTTP_200_OK)
        
        except Application.DoesNotExist:
            return Response({"error": "Invalid API Key"}, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)