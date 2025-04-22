from rest_framework.authentication import BaseAuthentication
from .utils import PermissionValidator
from rest_framework.exceptions import AuthenticationFailed

class ResourceServerAuthentication(BaseAuthentication):
    """
    Custom authentication for resource server that verifies both:
    1. Application permissions (via x-api-key)
    2. User permissions (via Authorization header)
    """
    def authenticate(self, request):
        # Extract required headers
        api_key = request.headers.get('x-api-key')
        user_token = self._extract_user_token(request)
        resource = request.headers.get('x-resource')
        sub_resource = request.headers.get('x-sub-resource')

        auth_results = {
            'application': None,
            'user': None
        }

        # First verify application permissions
        if api_key and resource:
            try:
                app_auth = PermissionValidator.check_application_permission(api_key, resource)
                auth_results['application'] = app_auth
            except AuthenticationFailed as e:
               
                if not user_token:
                    raise  # If no user token provided, fail completely

        # Then verify user permissions if token exists
        if user_token and resource and sub_resource:
            try:
                user_auth = PermissionValidator.check_user_permission(
                    user_token, api_key, resource, sub_resource
                )
                auth_results['user'] = user_auth
            except AuthenticationFailed as e:
                if not auth_results.get('application'):
                    raise  # Fail if neither application nor user auth succeeded

        # At least one authentication method must succeed
        if not auth_results['application'] and not auth_results['user']:
            raise AuthenticationFailed('Neither application nor user authentication succeeded')

        # Return auth tuple (user, auth_data)
        # We'll return a custom user object containing both auth results
        user = self._create_user_object(auth_results)
        return (user, None)

    def _extract_user_token(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header:
            return None

        try:
            auth_type, token = auth_header.split()
            if auth_type.lower() == 'token':
                return token
        except ValueError:
            return None

    def _create_user_object(self, auth_results):
        """
        Create a unified user object containing both application and user auth data
        """
        class AuthUser:
            def __init__(self, auth_data):
                self.is_authenticated = True
                self.auth_data = auth_data
                self.is_application = auth_data['application'] is not None
                self.is_user = auth_data['user'] is not None

                if auth_data['user']:
                    self.id = auth_data['user'].get('user', {}).get('id')
                    self.email = auth_data['user'].get('user', {}).get('email')
                    self.permissions = auth_data['user'].get('permissions', {})
                elif auth_data['application']:
                    self.id = auth_data['application'].get('application', {}).get('id')
                    self.name = auth_data['application'].get('application', {}).get('name')
                    self.permissions = auth_data['application'].get('permissions', [])

        return AuthUser(auth_results)

    def authenticate_header(self, request):
        return 'Token'