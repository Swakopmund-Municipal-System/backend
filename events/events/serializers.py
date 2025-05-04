"""
Serializers for the Calendar/Events Microservice
"""
from rest_framework import serializers
from .models import (
    Event, Location, Organizer, Department, Tag,
    Attendee, Attachment, RecurringPattern, EventChangeLog
)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class OrganizerSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = Organizer
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'


class RecurringPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringPattern
        fields = '__all__'


class EventChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventChangeLog
        fields = '__all__'


class EventListSerializer(serializers.ModelSerializer):
    location_name = serializers.ReadOnlyField(source='location.name')
    organizer_name = serializers.ReadOnlyField(source='organizer.name')
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'start_time', 'end_time', 'location_name',
            'organizer_name', 'status', 'is_public', 'is_featured', 'tags'
        ]


class EventDetailSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    organizer = OrganizerSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    attendees = AttendeeSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    recurring_pattern = RecurringPatternSerializer(source='recurringpattern', read_only=True)

    # Writable ID fields for updates
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='location', write_only=True, required=False
    )
    organizer_id = serializers.PrimaryKeyRelatedField(
        queryset=Organizer.objects.all(), source='organizer', write_only=True, required=False
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), source='tags', write_only=True, many=True, required=False
    )
    department_ids = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source='departments', write_only=True, many=True, required=False
    )

    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'location_id': {'write_only': True},
            'organizer_id': {'write_only': True},
            'tag_ids': {'write_only': True},
            'department_ids': {'write_only': True}
        }

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        departments_data = validated_data.pop('departments', [])

        event = Event.objects.create(**validated_data)

        if tags_data:
            event.tags.set(tags_data)
        if departments_data:
            event.departments.set(departments_data)

        return event

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        departments_data = validated_data.pop('departments', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if tags_data is not None:
            instance.tags.set(tags_data)
        if departments_data is not None:
            instance.departments.set(departments_data)

        return instance