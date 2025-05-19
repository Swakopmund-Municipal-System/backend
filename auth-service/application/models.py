from django.db import models
from django.conf import settings
from django.utils import timezone
from knox.models import AuthToken
from django.contrib.auth.hashers import make_password, check_password
import uuid
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=128, unique=True)
    api_key_expiration = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Displaying the plaintext API key in the admin interface
    _api_key_plain = None

    def __str__(self):
        return self.name

    def generate_api_key(self):
        plaintext_key = uuid.uuid4().hex
        self.api_key = make_password(plaintext_key)
        self.api_key_expiration = timezone.now() + timezone.timedelta(days=365*10)
        self._api_key_plain = plaintext_key
        return plaintext_key

    @property
    def display_key(self):
        if self._api_key_plain:

            return f"{self._api_key_plain} (Copy as it will not be shown again)"
        return "•••••••• (Hidden for security)"

    def check_api_key(self, key):
        return check_password(key, self.api_key)

class Resource(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class SubResource(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='sub_resources')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    allow_anonymous = models.BooleanField(default=False)

    class Meta:
        unique_together = ('resource', 'name')

    def __str__(self):
        return f"{self.resource.name}.{self.name}"


class ApplicationResourcePermission(models.Model):
    PERMISSION_CHOICES = [
        ('read', 'Read'),
        ('write', 'Write'),
        ('admin', 'Admin'),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    permission = ArrayField(models.CharField(max_length=10, choices=PERMISSION_CHOICES))

    class Meta:
        unique_together = ('application', 'resource')

    def __str__(self):
        return f"{self.application.name} - {self.resource.name} ({self.permission})"
