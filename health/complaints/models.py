# models.py
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

class Complaint(models.Model):
    complaint_id = models.CharField(primary_key=True, max_length=100, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('open', _('Open')),
        ('in_progress', _('In Progress')),
        ('resolved', _('Resolved')),
        ('closed', _('Closed')),
    ], default='open')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, editable=False)
    updated_by = models.CharField(max_length=50, editable=False)
    
    def __str__(self) -> str:
        return self.title
    
class ComplaintImage(models.Model):
    complaint = models.ForeignKey(Complaint, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='complaint_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __str__(self) -> str:
        return f"Image for {self.complaint.title}"