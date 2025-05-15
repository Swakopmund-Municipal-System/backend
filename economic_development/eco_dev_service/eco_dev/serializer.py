from rest_framework.serializers import ModelSerializer
from .models import BusinessRegApplication

class BusinessRegApplicationSerializer(ModelSerializer):
    class Meta:
        model = BusinessRegApplication
        fields = [
            "id",
            "name",
            "description",
            "location",
            "business_type",
            "image_url",
            "website_url",
            "is_approved",
            "date_reviewed",
            "approved_by",
            "comment",
            "created_at",
            "updated_at",
        ]

