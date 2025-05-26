import os
import requests
from fastapi import HTTPException, Header
from typing import Optional, Dict, Any

class AuthenticationFailed(Exception):
    pass

class PermissionValidator:
    @staticmethod
    def check_user_permission(user_token: str, api_key: str, resource: str, sub_resource: str) -> Dict[str, Any]:
        """
        Validate user permissions with the authentication service
        """
        auth_server_url = os.getenv("AUTH_SERVER_URL", "http://authentication:9080")
        
        headers = {
            "Authorization": f"Bearer {user_token}",
            "X-API-Key": api_key
        }
        
        payload = {
            "resource": resource,
            "sub_resource": sub_resource
        }
        
        try:
            response = requests.post(
                f"{auth_server_url}/api/auth/validate-permission/",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise AuthenticationFailed(f"Authentication failed: {response.text}")
                
        except requests.RequestException as e:
            raise AuthenticationFailed(f"Auth service unavailable: {str(e)}")

class PropertyAuthenticator:
    """
    Authentication class for Property Management Service
    """
    
    def authenticate(self, authorization: Optional[str] = None, x_api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Authenticate requests for property management endpoints
        """
        auth_results = {'application': None, 'user': None}
        
        # Extract token from Authorization header
        user_token = None
        if authorization and authorization.startswith('Bearer '):
            user_token = authorization.split(' ')[1]
        
        api_key = x_api_key
        
        # For property services, we use 'property' as resource
        resource = "property"
        
        # Try application authentication first
        if api_key:
            try:
                app_auth = PermissionValidator.check_user_permission(
                    user_token or "", api_key, resource, "property"
                )
                auth_results['application'] = app_auth
            except AuthenticationFailed:
                pass  # Continue to user auth
        
        # Try user authentication
        if user_token:
            try:
                user_auth = PermissionValidator.check_user_permission(
                    user_token, api_key or "", resource, "property"
                )
                auth_results['user'] = user_auth
            except AuthenticationFailed as e:
                if not auth_results.get('application'):
                    raise HTTPException(status_code=401, detail=str(e))
        
        # At least one authentication method must succeed
        if not auth_results['application'] and not auth_results['user']:
            raise HTTPException(status_code=401, detail='Authentication required')
        
        return auth_results

# Global authenticator instance
property_authenticator = PropertyAuthenticator()

def get_current_user(
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
) -> Dict[str, Any]:
    """
    FastAPI dependency for authentication
    """
    return property_authenticator.authenticate(authorization, x_api_key)

def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
) -> Optional[Dict[str, Any]]:
    """
    FastAPI dependency for optional authentication (for anonymous endpoints)
    """
    try:
        return property_authenticator.authenticate(authorization, x_api_key)
    except HTTPException:
        return None  # Allow anonymous access 