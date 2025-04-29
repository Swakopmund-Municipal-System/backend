# Authentication Service

The authentication service is built to use application authentication as well as user authentication

To connect the service to the frontend clients, follow these steps.

1. Create an application via the ```api/auth/application``` endpoint. This will create your application and provide you with the application api key. 
- To make a request, the body needs to contain the application name as follows

```json
{
    "name": "Application Name"
}
```

2. Once created, all requests to the backend must contain the API key in the header ```X-API-KEY``` as they will be validated to determine if the application has the correct permissions. 
- Permissions are to be assigned by system administrator through the Django Admin Panel appropriately

When making calls to the backend and authenticating calls, each service should redirect the call to the authentication server to validate it before proceeding. 

Here is an example of how you can authenticate a call:

```python
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
        user = self._create_user_object(auth_results)
        return (user, None)
```