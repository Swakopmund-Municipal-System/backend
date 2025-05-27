from django.contrib import admin
from .models import (
    Location,
    Department,
    Organizer,
    Tag,
    Event,
    EventChangeLog,
    Attendee,
    Attachment,
    RecurringPattern
)

# Register your models here.
admin.site.register(Location)
admin.site.register(Department)
admin.site.register(Organizer)
admin.site.register(Tag)
admin.site.register(Event)
admin.site.register(EventChangeLog)
admin.site.register(Attendee)
admin.site.register(Attachment)
admin.site.register(RecurringPattern)