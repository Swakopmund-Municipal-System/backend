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

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'capacity', 'is_accessible')
    list_filter = ('is_accessible', 'city')
    search_fields = ('name', 'address')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'contact_phone')
    search_fields = ('name', 'description')

@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'email')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'location', 'status', 'is_public', 'is_featured')
    list_filter = ('status', 'is_public', 'is_featured', 'tags', 'departments')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags', 'departments')
    date_hierarchy = 'start_time'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(EventChangeLog)
class EventChangeLogAdmin(admin.ModelAdmin):
    list_display = ('event', 'field_name', 'changed_at', 'processed_by_notification_service')
    list_filter = ('processed_by_notification_service',)
    readonly_fields = ('changed_at',)
    date_hierarchy = 'changed_at'

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event', 'registration_date', 'attended')
    list_filter = ('attended', 'notification_preference')
    search_fields = ('name', 'email', 'event__title')

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'file_type', 'uploaded_at')
    list_filter = ('file_type',)
    search_fields = ('name', 'event__title')

@admin.register(RecurringPattern)
class RecurringPatternAdmin(admin.ModelAdmin):
    list_display = ('event', 'frequency', 'interval', 'end_date')
    list_filter = ('frequency',)
    search_fields = ('event__title',)