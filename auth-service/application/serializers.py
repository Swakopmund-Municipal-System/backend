from rest_framework import serializers
from knox.models import AuthToken
from .models import Application, Resource, SubResource, ApplicationResourcePermission

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'name', 'api_key', 'api_key_expiration', 'is_active')
        read_only_fields = ('api_key', 'api_key_expiration')

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class SubResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubResource
        fields = '__all__'

class ApplicationResourcePermissionSerializer(serializers.ModelSerializer):
    resource = ResourceSerializer(read_only=True)
    
    class Meta:
        model = ApplicationResourcePermission
        fields = '__all__'