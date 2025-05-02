from django.contrib import admin
from .models import InterestingPlace, InterestingPlaceImage

# Register your models here.
admin.register(InterestingPlace, InterestingPlaceImage)