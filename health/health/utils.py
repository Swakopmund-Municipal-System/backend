# permissions.py
import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
import logging

logger = logging.getLogger(__name__)

class PermissionValidator:
    @staticmethod
    def check_user_permission(user_token, api_key, resource, sub_resource):
        """
        Verify user permissions by calling auth server endpoint
        """
        headers = {
            'Authorization': f'Token {user_token}',
            'x-api-key': api_key,
            'x-resource': resource,
            'x-sub-resource': sub_resource
        }

        try:
            response = requests.post(
                f'{settings.AUTH_SERVER_URL}/api/auth/user/check-user-permission/',
                headers=headers,
                timeout=3
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                raise PermissionDenied(response.json().get('error', 'Permission denied'))
            else:
                raise AuthenticationFailed(response.json().get('error', 'Authentication failed'))

        except requests.Timeout:
            logger.error("Auth server timeout during user permission check")
            raise AuthenticationFailed('Authentication service unavailable')
        except requests.RequestException as e:
            logger.error(f"Auth server error during user permission check: {str(e)}")
            raise AuthenticationFailed('Failed to verify user permissions')

    @staticmethod
    def check_application_permission(api_key, resource):
        """
        Verify application permissions by calling auth server endpoint
        """
        headers = {
            'x-api-key': api_key,
            'x-resource': resource
        }

        try:
            response = requests.post(
                f'{settings.AUTH_SERVER_URL}/api/auth/application/check_application_permission/',
                headers=headers,
                timeout=3
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                raise PermissionDenied(response.json().get('error', 'Application permission denied'))
            else:
                raise AuthenticationFailed(response.json().get('error', 'Application authentication failed'))

        except requests.Timeout:
            logger.error("Auth server timeout during application permission check")
            raise AuthenticationFailed('Authentication service unavailable')
        except requests.RequestException as e:
            logger.error(f"Auth server error during application permission check: {str(e)}")
            raise AuthenticationFailed('Failed to verify application permissions')