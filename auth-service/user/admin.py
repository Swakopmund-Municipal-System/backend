from django.db import models
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import User, UserType, UserResourcePermission
from application.models import SubResource
from unfold.admin import ModelAdmin
from .filters import PermissionFilter


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "home_address", "user_types"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, and allows editing the password.
    """
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Password")

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "is_active", "user_types"]

    def clean_password(self):
        # Return the initial password value if no new password is provided
        return self.cleaned_data["password"] or self.instance.password

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["password"]:
            user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):  # Use both BaseUserAdmin and ModelAdmin from Unfold
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model
    list_display = ["email", "first_name", "last_name", "is_active", "is_municipal_staff", "primary_user_type_display"]
    list_filter = ["is_active", "is_municipal_staff", "user_types"]
    search_fields = ["email", "first_name", "last_name", "home_address"]
    ordering = ["email"]

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ('Personal info', {"fields": ["first_name", "last_name", "home_address"]}),
        ('Permissions', {"fields": ["is_active", "user_types", "is_municipal_staff"]}),
        ('Important dates', {"fields": ["last_login", "date_joined"]}),
    ]

    def primary_user_type_display(self, obj):
        return obj.primary_user_type
    primary_user_type_display.short_description = "Primary User Type"



    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "first_name", "last_name", "home_address", "password1", "password2", "user_types"],
            },
        ),
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ["last_login", "date_joined", "is_municipal_staff"]
        return []

    filter_horizontal = ["user_types"]  # Use filter_horizontal for many-to-many fields


@admin.register(UserType)
class UserTypeAdmin(ModelAdmin):
    list_display = ["name", "description", "is_municipal_staff"]
    search_fields = ["name", "description"]
    list_filter = ["is_municipal_staff"]


class UserResourcePermissionForm(forms.ModelForm):
    class Meta:
        model = UserResourcePermission
        fields = '__all__'
        widgets = {
            'permission': forms.CheckboxSelectMultiple
        }

@admin.register(UserResourcePermission)
class UserResourcePermissionAdmin(ModelAdmin):
    form = UserResourcePermissionForm
    list_display = ["user_type", "sub_resource", "display_permissions"]
    list_filter = [PermissionFilter, "user_type", "sub_resource__name"]
    search_fields = ["user_type__name", "sub_resource__name"]

    fieldsets = [
        (None, {"fields": ["user_type", "sub_resource"]}),
        ('Permissions', {"fields": ["permission"]}),
    ]

    def display_permissions(self, obj):
        return ", ".join(obj.permission) if obj.permission else "-"
    display_permissions.short_description = "Permissions"

# Unregister the Group model from admin
admin.site.unregister(Group)
