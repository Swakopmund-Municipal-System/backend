from django.db import models
from django.utils.timezone import now

BUSINESS_TYPES = {
    'S': 'Service',
    'P': 'Product',
    'H': 'Hospitality',
}

# Create your models here.
class BusinessRegApplication(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    business_type = models.CharField(choices=BUSINESS_TYPES)
    image_url = models.CharField(max_length=255)
    website_url = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    date_reviewed = models.DateTimeField(null=True)
    approved_by = models.CharField(null=True)
    comment = models.CharField(max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
