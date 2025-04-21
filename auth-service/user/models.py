from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from .managers import UserManager
from application.models import SubResource


USER_TYPES = (
    ('resident', 'Resident'),
    ('tourist', 'Tourist'),
    ('property-developer', 'Property Developer'),
    ('planning-department')
)
# Create your models here.

class UserType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)
    is_municipal_staff = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    user_types = models.ManyToManyField(UserType, related_name='users')
    is_municipal_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        """
        Designates the municipal staff property based on the user types
        """
        super().save(*args, **kwargs)
        
        if hasattr(self, 'user_types'):
            new_value = self.user_types.filter(is_municipal_staff=True).exists()
            
            if new_value != self.is_municipal_staff:
                # Avoid infinite recursion by using update()
                User.objects.filter(pk=self.pk).update(is_municipal_staff=new_value)
                self.is_municipal_staff = new_value
        
    @property
    def primary_user_type(self):
        """
        Returns the first user type or a default if none exists
        Useful for backward compatibility
        """
        return self.user_types.first().name if self.user_types.exists() else 'resident'
    
class UserResourcePermission(models.Model):
    PERMISSION_CHOICES = [
        ('read', 'Read'),
        ('write', 'Write'),
        ('admin', 'Admin'),
    ]
    sub_resource = models.ForeignKey(SubResource, on_delete=models.CASCADE)
    permission = ArrayField(models.CharField(max_length=100, choices=PERMISSION_CHOICES))
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, blank=True)

        
    def __str__(self):
        return f"{self.user_type} - {self.sub_resource} ({self.permission})"
