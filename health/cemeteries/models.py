from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.
class CemeteryPlot(models.Model):
    plot_id = models.CharField(primary_key=True, max_length=100, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, editable=False)
    updated_by = models.CharField(max_length=50, editable=False)
    
    def __str__(self) -> str:
        return self.title
    
