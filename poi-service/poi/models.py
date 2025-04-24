from django.db import models
from django.utils.timezone import now

class InterestingPlace(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=300)
    location = models.CharField(max_length=200) # TODO: Change to support coordinate data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class InterestingPlaceImage(models.Model):
    place_id = models.ForeignKey(InterestingPlace, on_delete=models.CASCADE)
    image_url = models.CharField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



