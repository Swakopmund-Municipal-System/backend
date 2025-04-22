# health/models.py
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class User(AbstractBaseUser):
    """
    Proxy user model for authentication only
    """
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=20, default='guest')
    
    USERNAME_FIELD = 'email'
    
    class Meta:
        # Setting this as a proxy/abstract model since we're not using it for DB operations
        abstract = True