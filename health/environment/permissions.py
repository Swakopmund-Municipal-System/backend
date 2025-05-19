from rest_framework import permissions

class IsHealthAdmin(permissions.BasePermission):
    """
    Health Admin Users Permission Class
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class UserHasAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request, 'user_data'):
            return False
            
        # Check user properties for access control
        # For example, check user role
        user_role = request.user_data.get('role', '')
        
        # You can implement custom logic based on the API endpoint
        if view.basename == 'health_records':
            return user_role in ['doctor', 'admin']
        elif view.basename == 'appointments':
            return user_role in ['doctor', 'patient', 'admin']
            
        return False
    
class UserAuthenticatedPermission(permissions.BasePermission):
    """
    Verifies that the user was authenticated via UserAuthentication
    """
    def has_permission(self, request, view):
        # Check if the user has expected attributes from UserAuthentication
        return hasattr(request.user, 'email') and request.user.email != ''
