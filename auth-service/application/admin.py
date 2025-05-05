from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from .models import Application, Resource, SubResource, ApplicationResourcePermission
from django import forms
from .filters import AppPermissionFilter

class ApplicationAdminForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'is_active']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk:
            plaintext_key = instance.generate_api_key()
            instance._api_key_plain = plaintext_key
        if commit:
            instance.save()
        return instance

@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    form = ApplicationAdminForm
    list_display = ('name', 'display_key', 'is_active', 'api_key_expiration', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

    fields = ('name', 'is_active', 'display_key', 'api_key_expiration',
              'created_at', 'updated_at')

    def get_fields(self, request, obj=None):
        if obj:  # Existing object
            return ['name', 'is_active', 'display_key',
                    'api_key_expiration', 'created_at', 'updated_at']
        return ['name', 'is_active']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('display_key', 'api_key_expiration', 'created_at', 'updated_at')
        return ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.generate_api_key()
        super().save_model(request, obj, form, change)
        if hasattr(obj, '_api_key_plain') and obj._api_key_plain:
            from django.contrib import messages
            messages.warning(
                request,
                f"{obj.name} {obj._api_key_plain} key has been generated. Copy before saving the form again."
            )

@admin.register(Resource)
class ResourceAdmin(ModelAdmin):
    list_display = ('name', 'description', 'sub_resources_count')
    search_fields = ('name', 'description')

    def sub_resources_count(self, obj):
        return obj.sub_resources.count()
    sub_resources_count.short_description = 'Sub Resources'

@admin.register(SubResource)
class SubResourceAdmin(ModelAdmin):
    list_display = ('name', 'resource', 'description', 'allow_anonymous')
    list_filter = ('resource', 'allow_anonymous')
    search_fields = ('name', 'description', 'resource__name')

class ApplicationResourcePermissionForm(forms.ModelForm):
    permission = forms.MultipleChoiceField(
        choices=ApplicationResourcePermission.PERMISSION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = ApplicationResourcePermission
        fields = '__all__'
        # widgets = {
        #     'permission': forms.CheckboxSelectMultiple
        # }

@admin.register(ApplicationResourcePermission)
class ApplicationResourcePermissionAdmin(ModelAdmin):
    form = ApplicationResourcePermissionForm
    list_display = ('application', 'resource', 'display_permissions')
    list_filter = (AppPermissionFilter, 'application', 'resource')
    search_fields = ('application__name', 'resource__name')

    def display_permissions(self, obj):
        return ", ".join(obj.permission) if obj.permission else "-"
    display_permissions.short_description = "Permissions"
