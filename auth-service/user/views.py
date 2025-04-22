# django imports
from django.contrib.auth import login
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
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from rest_framework.authtoken.serializers import AuthTokenSerializer

# Knox Imports
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication

# App imports
from application.models import Application, Resource, SubResource, ApplicationResourcePermission
from .models import User, UserType, UserResourcePermission
from .serializers import UserCreateSerializer, UserSerializer, AuthenticateUserSerializer

# Create your views here.
class CheckUserPermission(APIView):
    """
    Verify if the user has permission to access the requested resource.
    First checks if resource allows anonymous access, then checks user permissions if needed.
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
        # Extract headers from the request
        headers = {
            'x-api-key': request.headers.get('X-API-KEY'),
            'authorization': request.headers.get('Authorization'),
            'x-resource': request.headers.get('X-RESOURCE'),
            'x-sub-resource': request.headers.get('X-SUB-RESOURCE'),
            'x-method': request.headers.get('X-METHOD', 'GET').upper(),
        }

        # Validate required headers
        if not headers['x-resource'] or not headers['x-sub-resource']:
            return Response(
                {"error": "x-resource and x-sub-resource headers are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # First check if the resource allows anonymous access
        try:
            sub_resource = SubResource.objects.get(
                resource__name=headers['x-resource'],
                name=headers['x-sub-resource'],
                allow_anonymous=True
            )
            
            # For anonymous access, only allow GET requests (read-only)
            if headers['x-method'] == 'GET':
                return Response({
                    'status': "authorised",
                    'anonymous': True,
                    'permission': 'read',
                    'message': "Anonymous read access granted"
                }, status=status.HTTP_200_OK)
            
            return Response({
                "error": "Anonymous access only allows GET requests"
            }, status=status.HTTP_403_FORBIDDEN)
            
        except SubResource.DoesNotExist:
            pass  # Resource doesn't allow anonymous access, proceed to check auth

        # If we get here, the resource requires authentication
        if not headers['authorization']:
            return Response(
                {"error": "Authentication required for this resource"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Authenticate the user
        try:
            from knox.auth import TokenAuthentication
            knox_auth = TokenAuthentication()
            user, _ = knox_auth.authenticate_credentials(
                headers['authorization'].split(' ')[-1].encode('utf-8')
            )
        except Exception as e:
            return Response(
                {"error": "Invalid authentication token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Get required permission based on HTTP method
        required_permission = self.METHOD_TO_PERMISSION.get(headers['x-method'], 'read')
        permission_levels = ['read', 'write', 'admin']

        # Check user permissions through their user types
        user_types = user.user_types.all()
        if not user_types.exists():
            return Response(
                {"error": "User has no assigned types"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get all permissions for this user's types and the requested resource
        type_permissions = UserResourcePermission.objects.filter(
            user_type__in=user_types,
            sub_resource__resource__name=headers['x-resource'],
            sub_resource__name=headers['x-sub-resource']
        )

        if not type_permissions.exists():
            return Response(
                {"error": "No permissions found for user types"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Collect all permission levels from all relevant permissions
        all_permissions = []
        for perm in type_permissions:
            all_permissions.extend(perm.permission)

        if not all_permissions:
            return Response(
                {"error": "No valid permissions found"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get the highest permission available
        highest_permission = max(
            all_permissions,
            key=lambda p: permission_levels.index(p)
        )

        if permission_levels.index(highest_permission) >= permission_levels.index(required_permission):
            return Response({
                'status': "authorised",
                'user': {'id': user.id, 'email': user.email},
                'permission': highest_permission,
                'user_types': [ut.name for ut in user_types]
                
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": f"Requires {required_permission} permission but only has {highest_permission}"
            }, status=status.HTTP_403_FORBIDDEN)


        
class LoginView(KnoxLoginView):
    """
    Override the Knox LoginView.
    """
    serialzer_class = AuthenticateUserSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
    
    
class CreateUserView(APIView):
    """
    Create a new user
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        
        
class ValidateUserTokenView(APIView):
    """
    Validate the user token provided
    """        
    
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header:
            return Response({"error": "Authorization header is required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            auth_type, token = auth_header.split(' ')
            if auth_type != 'Token':
                return Response({"error": "Invalid authorization type"}, status=status.HTTP_401_UNAUTHORIZED)
        except ValueError:
            return Response({"error": "Invalid authorization header format"}, status=status.HTTP_401_UNAUTHORIZED)
        
        know_auth = TokenAuthentication()
        try:
            user, user_token = know_auth.authenticate_credentials(token.encode('utf-8'))
            
            user_info = {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_types': list(user.user_types.values_list('name', flat=True)),
            }    
            
            return Response({
                'status': "authorised",
                'user': user_info,
                'token_expiry': user_token.expiry if user_token else None,
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        
        