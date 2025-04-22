from django.contrib import admin

from .models import Application, Resource, SubResource, ApplicationResourcePermission
# Register your models here.
admin.site.register(Application)
admin.site.register(Resource)
admin.site.register(SubResource)
admin.site.register(ApplicationResourcePermission)
