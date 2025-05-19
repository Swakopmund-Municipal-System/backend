import uuid
from rest_framework import serializers
from .models import Complaint, ComplaintImage

class ComplaintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintImage
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

class ComplaintSerializer(serializers.ModelSerializer):
    images = ComplaintImageSerializer(many=True, required=False)
    
    class Meta:
        model = Complaint
        fields = [
            'complaint_id',
            'title',
            'description',
            'status',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'images'
        ]
        read_only_fields = [
            'complaint_id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]
        extra_kwargs = {
            'title': {
                'max_length': 50,
                'required': True
            },
            'description': {
                'required': True
            },
            'status': {
                'required': False
            }
        }

    def _get_authenticated_user(self):
        """Extract user info """
        request = self.context.get('request')
        if request and hasattr(request, 'user') and hasattr(request.user, 'auth_data'):
            auth_data = request.user.auth_data
            if auth_data.get('user'):
                return {
                    'id': auth_data['user']['user']['id'],
                    'email': auth_data['user']['user']['email'],
                    'user_types': auth_data['user'].get('user_types', [])
                }
            elif auth_data.get('application'):
                return {
                    'id': None,
                    'email': None,
                    'application': auth_data['application']['application']
                }
        return None

    def create(self, validated_data):
        user_info = self._get_authenticated_user()
        if user_info:
            if user_info.get('email'):
                validated_data['created_by'] = user_info['email']
                validated_data['updated_by'] = user_info['email']
            elif user_info.get('application'):
                validated_data['created_by'] = user_info['application']
                validated_data['updated_by'] = user_info['application']
        
        # Ensure complaint_id is generated if not provided
        if 'complaint_id' not in validated_data:
            validated_data['complaint_id'] = str(uuid.uuid4())
            
        # Handle image uploads
        images_data = self.context.get('request').FILES
        complaint = Complaint.objects.create(**validated_data)
        
        for image_data in images_data.getlist('images'):
            ComplaintImage.objects.create(
                complaint=complaint,
                image=image_data
            )
            
        return complaint

    def update(self, instance, validated_data):
        user_info = self._get_authenticated_user()
        if user_info:
            if user_info.get('email'):
                validated_data['updated_by'] = user_info['email']
            elif user_info.get('application'):
                validated_data['updated_by'] = user_info['application']
        
        # Handle image updates if needed (you might want to handle this separately)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Custom representation to include user_types if available"""
        representation = super().to_representation(instance)
        user_info = self._get_authenticated_user()
        
        if user_info and user_info.get('user_types'):
            representation['creator_user_types'] = user_info['user_types']
            
        return representation