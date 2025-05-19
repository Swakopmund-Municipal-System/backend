from django.contrib.admin import SimpleListFilter
from .models import ApplicationResourcePermission

class AppPermissionFilter(SimpleListFilter):
    title = 'permission'
    parameter_name = 'permission_contains'

    def lookups(self, request, model_admin):
        # Returns a list of tuples for the filter options
        return [
            ('read', 'Read'),
            ('write', 'Write'),
            ('admin', 'Admin'),
        ]

    def queryset(self, request, queryset):
        # Returns the filtered queryset based on the value provided in the query string
        if self.value():
            # Use the contains lookup for ArrayField
            return queryset.filter(permission__contains=[self.value()])
        return queryset
