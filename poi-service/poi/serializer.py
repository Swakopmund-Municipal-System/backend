from rest_framework.serializers import ModelSerializer
from .models import InterestingPlace, InterestingPlaceImage

class InterestingPlaceSerializer(ModelSerializer):
    class Meta:
        model = InterestingPlace
        fields = [
            "id",
            "name",
            "description",
            "location",
            "created_at",
            "updated_at",
        ]

class InterestingPlaceImageSerializer(ModelSerializer):
    class Meta:
        model = InterestingPlaceImage
        fields = [
            "id",
            "place_id",
            "image_url",
            "created_at",
            "updated_at",
        ]