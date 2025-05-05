"""
Models for Municipal Calendar/Events Microservice using Django ORM
Events will publish to a separate notifications microservice
"""
from django.db import models
from django.utils import timezone


class Location(models.Model):
    """Location model for event venues"""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    is_accessible = models.BooleanField(default=True)
    contact_info = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    """Department model for municipal departments"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Organizer(models.Model):
    """Organizer model for event coordinators"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    department = models.ForeignKey(Department, related_name='organizers', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tag model for categorizing events"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    """Event model for municipal events"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.ForeignKey(Location, related_name='events', on_delete=models.SET_NULL, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    registration_required = models.BooleanField(default=False)
    max_attendees = models.IntegerField(null=True, blank=True)
    organizer = models.ForeignKey(Organizer, related_name='events', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Fields for integration with notification microservice
    notification_sent = models.BooleanField(default=False)
    last_notification_sent_at = models.DateTimeField(null=True, blank=True)

    # Many-to-many relationships
    tags = models.ManyToManyField(Tag, related_name='events', blank=True)
    departments = models.ManyToManyField(Department, related_name='events', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_time']

    def save(self, *args, **kwargs):
        """Override save to detect changes that should trigger notifications"""
        is_new = self.pk is None

        # Handle status changes for existing events
        if not is_new:
            old_instance = Event.objects.get(pk=self.pk)
            status_changed = old_instance.status != self.status
            time_changed = old_instance.start_time != self.start_time or old_instance.end_time != self.end_time

            # Mark for notification if key fields changed
            if status_changed or time_changed:
                self.notification_sent = False

        super().save(*args, **kwargs)


class EventChangeLog(models.Model):
    """Log of event changes for notification tracking"""
    event = models.ForeignKey(Event, related_name='change_logs', on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    changed_at = models.DateTimeField(default=timezone.now)
    processed_by_notification_service = models.BooleanField(default=False)

    def __str__(self):
        return f"Change to {self.event.title}.{self.field_name} at {self.changed_at}"

    class Meta:
        ordering = ['-changed_at']


class Attendee(models.Model):
    """Attendee model for event participants"""
    event = models.ForeignKey(Event, related_name='attendees', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    registration_date = models.DateTimeField(default=timezone.now)
    attended = models.BooleanField(default=False)

    # Field for notification preferences
    notification_preference = models.CharField(max_length=20, default='email',
                                              choices=[('email', 'Email'),
                                                      ('sms', 'SMS'),
                                                      ('both', 'Both'),
                                                      ('none', 'None')])

    def __str__(self):
        return f"{self.name} - {self.event.title}"

    class Meta:
        unique_together = ['event', 'email']


class Attachment(models.Model):
    """Attachment model for event documents/files"""
    event = models.ForeignKey(Event, related_name='attachments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='event_attachments/')
    file_type = models.CharField(max_length=100, blank=True)
    size = models.IntegerField(help_text="File size in bytes", blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class RecurringPattern(models.Model):
    """RecurringPattern model for repeating events"""
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
    interval = models.IntegerField(default=1, help_text="Every X days/weeks/months/years")
    days_of_week = models.CharField(max_length=20, blank=True, help_text="Comma-separated days (1-7)")
    day_of_month = models.IntegerField(null=True, blank=True)
    month_of_year = models.IntegerField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True, help_text="Number of occurrences")

    def __str__(self):
        return f"{self.get_frequency_display()} - {self.event.title}"