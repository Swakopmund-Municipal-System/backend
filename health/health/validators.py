from oauth2_provider.oauth2_validators import OAuth2Validator

class OAuth2Validator(OAuth2Validator):
    def validate_bearer_token(self, token, scopes, request):
        
        is_valid = super().validate_bearer_token(token, scopes, request)
        
        if is_valid:
            introspection_data = getattr(request.auth, '_introspection_data', {})
            
            for attr in ['user_id', 'username', 'is_staff', 'is_superuser']:
                if attr in introspection_data:
                    setattr(request.auth, attr, introspection_data[attr])
                    
        return is_valid