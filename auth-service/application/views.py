

from rest_framework.permissions import AllowAny
# Rest Framework Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# App Imports
from .models import Application, ApplicationResourcePermission
from .serializers import ApplicationSerializer

from django.utils import timezone


# API Documentation
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes


# Views
class ApplicationListView(APIView):
    """
    List all applications or create a new application.
    """

    @extend_schema(
        request=ApplicationSerializer,
        responses={200: ApplicationSerializer(many=True)},
        description="List all applications"
    )
    def get(self, request):
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=ApplicationSerializer,
        responses={201: ApplicationSerializer},
        description="Create a new application"
    )
    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()
            return Response(ApplicationSerializer(application).data,
                            status=status.HTTP_201_CREATED)
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

        if not api_key:
            return Response({"error": "Missing API key"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            applications = Application.objects.filter(is_active=True)
            application = None

            for app in applications:
                if app.check_api_key(api_key):
                    application = app
                    break

            if not application:
                return Response({"error": "Invalid API Key"},
                                status=status.HTTP_403_FORBIDDEN)

            if application.api_key_expiration < timezone.now():
                return Response({"error": "API Key has expired"},
                                status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_403_FORBIDDEN
                            )

        requested_resource = request.headers.get('x-resource')
        # Default to GET if not specified
        http_method = request.headers.get('x-method', 'GET').upper()

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
            print(f"Highest App Permission: {highest_app_permission}")
            if permission_hierarchy.index(highest_app_permission) < permission_hierarchy.index(required_permission):
                return Response({"error": "Permission denied, insufficient permissions"},
                                status=status.HTTP_403_FORBIDDEN
                                )

        except ApplicationResourcePermission.DoesNotExist:
            return Response({"error": "Permission denied, resource permission not found"},
                            status=status.HTTP_403_FORBIDDEN
                            )

        return Response(
            {
                "status": "authorised",
                "application": application.name,
                "resource": requested_resource,
                "permission": highest_app_permission,
            }, status=status.HTTP_200_OK
        )


class ValidateAPIKeyView(APIView):
    """
    Validate the API key and check its expiration.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='X-API-KEY',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                description='API key for authentication',
                required=True
            )
        ],
        responses={
            200: OpenApiResponse(
                description="API key is valid",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Success response",
                        value={
                            "status": "valid",
                            "application": {
                                "id": 1,
                                "name": "Example Application"
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Missing API key",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Missing API key",
                        value={"error": "Invalid API key"}
                    )
                ]
            ),
            403: OpenApiResponse(
                description="Invalid or expired API key",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Invalid API key",
                        value={"error": "Invalid API Key"}
                    ),
                    OpenApiExample(
                        name="Expired API key",
                        value={"error": "API Key has expired"}
                    )
                ]
            ),
            500: OpenApiResponse(
                description="Internal server error",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Server error",
                        value={"error": "Internal server error occurred"}
                    )
                ]
            )
        },
        auth=None,
        summary="Validate API key",
        description="""
        Validates an API key by checking:
        - Presence in X-API-KEY header
        - Existence in database
        - Active status (is_active=True)
        - Expiration date (if set)

        Returns application information if validation succeeds.
        """
    )
    def post(self, request):
        api_key = request.headers.get('X-API-KEY')

        if not api_key:
            return Response({"error": "Invalid API key"},
                            status=status.HTTP_400_BAD_REQUEST
                            )

        try:
            applications = Application.objects.filter(is_active=True)
            application = None

            for app in applications:
                if app.check_api_key(api_key):
                    application = app
                    break

            if not application:
                return Response({"error": "Invalid API Key"},
                                status=status.HTTP_403_FORBIDDEN
                                )

            if application.api_key_expiration and application.api_key_expiration < timezone.now():
                return Response({"error": "API Key has expired"},
                                status=status.HTTP_403_FORBIDDEN
                                )

            app_info = {
                'id': application.id,
                "name": application.name,
            }

            return Response({
                "status": "valid",
                "application": app_info,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )
