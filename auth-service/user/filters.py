from django.contrib.admin import SimpleListFilter
from .models import UserResourcePermission

class PermissionFilter(SimpleListFilter):
    title = 'permission'
    parameter_name = 'permission_contains'

    def lookups(self, request, model_admin):
        # Returns a list of tuples. The first element in each tuple is the coded value
        # for the option that will appear in the URL query. The second element is the
        # human-readable name for the option that will appear in the filter UI.
        return [
            ('read', 'Read'),
            ('write', 'Write'),
            ('admin', 'Admin'),
        ]

    def queryset(self, request, queryset):
        # Returns the filtered queryset based on the value
        # provided in the query string and retrievable via
        # `self.value()`.
        if self.value():
            # Use the contains lookup for ArrayField
            return queryset.filter(permission__contains=[self.value()])
        return queryset
