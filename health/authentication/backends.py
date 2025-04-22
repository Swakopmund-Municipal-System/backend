import requests
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
import httpx


class UserAuthentication(BaseAuthentication):
    def __init__(self):
        print("UserAuthentication class initialized")
        
    def authenticate(self, request):
        print("Begin authenticating users")
        user_token = request.META.get('HTTP_X_USER_TOKEN')
        
        print(request.META.get('HTTP_AUTHORIZATION'))
        if not user_token:
            print("No user token provided")
            return None
            
        try:
            print(f"Validating token with auth server at {settings.AUTH_SERVER_URL}")
            response = requests.get(
                f'{settings.AUTH_SERVER_URL}/api/auth/user/info',
                headers={'Authorization': f'Bearer {user_token}'}
            )
            
            print(f"Auth server response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"Auth server error: {response.text}")
                raise AuthenticationFailed('Invalid user token')
                
            user_data = response.json()
            print(f"Auth server response data: {user_data}")
            
            # Use AnonymousUser as a base for creating a user object
            user = User()  # Create an instance of the User model
            user.id = user_data.get('id')
            user.username = user_data.get('email')  # Set username to email for Django User model
            user.email = user_data.get('email')
            user.is_staff = user_data.get('is_staff', False)
            user.is_active = True
            
            # Manually set authentication status
            # This is crucial but doesn't actually work this way - see below
            # user.is_authenticated = True
            
            print(f"Created user object: {user}")
            return (user, None)
        except Exception as e:
            print(f"Authentication failed: {str(e)}")
            raise AuthenticationFailed(f'Failed to authenticate user: {str(e)}')