import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models



def create_initial_user_types(apps, schema_editor):
    """
    Initalise the UserType model with default user types.
    """
    UserType = apps.get_model('user', 'UserType')
    
    initial_types = [
        # Basic user types
        {'name': 'resident', 'description': 'Local resident', 'is_municipal_staff': False},
        {'name': 'tourist', 'description': 'Visitor to the area', 'is_municipal_staff': False},
        {'name': 'property-developer', 'description': 'Property developer', 'is_municipal_staff': False},
        
        # Municipal staff types (from Property & Land Management and other services)
        {'name': 'planning-department', 'description': 'Municipal planning staff', 'is_municipal_staff': True},
        {'name': 'building-inspector', 'description': 'Municipal building inspector', 'is_municipal_staff': True},
        {'name': 'environmental-officer', 'description': 'Environmental health officer', 'is_municipal_staff': True},
        {'name': 'funeral-home', 'description': 'Funeral home operator', 'is_municipal_staff': False},
        {'name': 'event-organizer', 'description': 'Community event organizer', 'is_municipal_staff': False},
        {'name': 'library-staff', 'description': 'Municipal library staff', 'is_municipal_staff': True},
        {'name': 'business-support', 'description': 'Economic development staff', 'is_municipal_staff': True},
        {'name': 'fire-department', 'description': 'Fire and safety officer', 'is_municipal_staff': True},
        {'name': 'law-enforcement', 'description': 'Municipal law enforcement', 'is_municipal_staff': True},
        {'name': 'waste-management', 'description': 'Waste management staff', 'is_municipal_staff': True},
        {'name': 'health-services', 'description': 'Public health staff', 'is_municipal_staff': True},
        {'name': 'community-services', 'description': 'Community services staff', 'is_municipal_staff': True},
        
        # Additional roles from the document
        {'name': 'business-owner', 'description': 'Local business owner', 'is_municipal_staff': False},
        {'name': 'restaurant-owner', 'description': 'Restaurant owner/manager', 'is_municipal_staff': False},
        {'name': 'accommodation-provider', 'description': 'Accommodation provider', 'is_municipal_staff': False},
    ]
    
    for type_data in initial_types:
        UserType.objects.create(**type_data)
        
        
        
def create_initial_user_permissions(apps, schema_editor):
    UserType = apps.get_model('user', 'UserType')
    Resource = apps.get_model('application', 'Resource')
    SubResource = apps.get_model('application', 'SubResource')
    UserResourcePermission = apps.get_model('user', 'UserResourcePermission')

    # Create all resources and subresources
    create_calendar_services(Resource, SubResource)
    create_activities_services(Resource, SubResource)
    create_places_services(Resource, SubResource)
    create_accommodation_services(Resource, SubResource)
    create_restaurants_services(Resource, SubResource)
    create_mapping_services(Resource, SubResource)
    create_weather_services(Resource, SubResource)
    create_property_services(Resource, SubResource)
    create_health_services(Resource, SubResource)
    create_community_services(Resource, SubResource)
    create_economic_services(Resource, SubResource)
    create_safety_services(Resource, SubResource)
    create_waste_services(Resource, SubResource)
    create_citizen_portal(Resource, SubResource)

    # Define permissions for each user type
    permissions_map = {
        # Basic user types
        'resident': {
            'events': ['read'],
            'comments': ['read', 'write'],
            'fetch-activities': ['read'],
            'modify-activities': ['read'],
            'review-activities': ['read', 'write'],
            'modify-activity-reviews': ['read', 'write'],
            'fetch-places': ['read'],
            'review-places': ['read', 'write'],
            'fetch-accommodation': ['read'],
            'review-accommodation': ['read', 'write'],
            'fetch-restaurants': ['read'],
            'review-restaurants': ['read', 'write'],
            'fetch-mapping': ['read'],
            'fetch-weather': ['read'],
            'property': ['read'],
            'environment-health': ['read'],
            'fetch-cemetery-health': ['read'],
            'complaint-health': ['read', 'write'],
            'books': ['read'],
            'borrow': ['read', 'write'],
            'register-business': ['read', 'write'],
            'fetch-attraction': ['read'],
            'fetch-events': ['read'],
            'report-incident': ['read', 'write'],
            'status-incident': ['read'],
            'fetch-schedule': ['read'],
            'report-pickup': ['read', 'write'],
            'fetch-recycling': ['read'],
            'bin': ['read', 'write'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'tourist': {
            'events': ['read'],
            'fetch-activities': ['read'],
            'modify-activities': ['read'],
            'review-activities': ['read', 'write'],
            'fetch-places': ['read'],
            'fetch-accommodation': ['read'],
            'fetch-restaurants': ['read'],
            'fetch-mapping': ['read'],
            'fetch-weather': ['read'],
            'property': ['read'],
            'environment-health': ['read'],
            'fetch-cemetery-health': ['read'],
            'books': ['read'],
            'fetch-attraction': ['read'],
            'fetch-events': ['read'],
            'status-incident': ['read'],
            'fetch-schedule': ['read'],
            'fetch-recycling': ['read'],
            'auth': ['read', 'write'],
        },
        'property-developer': {
            'property': ['read', 'write'],
            'property-admin': ['read'],
            'auth': ['read', 'write'],
        },

        # Municipal staff types
        'planning-department': {
            'property': ['read'],
            'property-admin': ['read', 'write', 'admin'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'building-inspector': {
            'property': ['read'],
            'property-admin': ['read', 'write', 'admin'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'environmental-officer': {
            'environment-health': ['read', 'write', 'admin'],
            'complaint-health': ['read', 'write', 'admin'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'funeral-home': {
            'fetch-cemetery-health': ['read'],
            'modify-cemetery-health': ['read', 'write'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'event-organizer': {
            'events': ['read', 'write'],
            'modify-events': ['read', 'write'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'library-staff': {
            'books': ['read', 'write', 'admin'],
            'borrow': ['read', 'write', 'admin'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'business-support': {
            'register-business': ['read', 'write', 'admin'],
            'modify-attraction': ['read', 'write', 'admin'],
            'fetch-attraction': ['read'],
            'modify-events': ['read', 'write', 'admin'],
            'fetch-events': ['read'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'fire-department': {
            'report-incident': ['read', 'write', 'admin'],
            'status-incident': ['read', 'write', 'admin'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'law-enforcement': {
            'report-incident': ['read', 'write', 'admin'],
            'status-incident': ['read', 'write', 'admin'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'waste-management': {
            'fetch-schedule': ['read'],
            'modify-schedule': ['read', 'write', 'admin'],
            'report-pickup': ['read', 'write', 'admin'],
            'fetch-recycling': ['read'],
            'modify-recycling': ['read', 'write', 'admin'],
            'bin': ['read', 'write', 'admin'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write','read','admin'],
        },
        'health-services': {
            'environment-health': ['read', 'write', 'admin'],
            'modify-cemetery-health': ['read', 'write', 'admin'],
            'fetch-cemetery-health': ['read'],
            'complaint-health': ['read', 'write', 'admin'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'community-services': {
            'books': ['read', 'write', 'admin'],
            'borrow': ['read', 'write', 'admin'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },

        # Business owners
        'business-owner': {
            'register-business': ['read', 'write'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'restaurant-owner': {
            'fetch-restaurants': ['read'],
            'review-restaurants': ['read', 'write', 'admin'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'accommodation-provider': {
            'fetch-accommodation': ['read'],
            'review-accommodation': ['read', 'write', 'admin'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        },
        'activities-provider': {
            'fetch-activities': ['read'],
            'modify-activities': ['read', 'write', 'admin'],
            'review-activities': ['read', 'write', 'admin'],
            'auth': ['read', 'write'],
            'missed-waste-pickups': ['write'],
        }
    }

    # Create the permissions
    create_permissions(UserResourcePermission, UserType, SubResource, permissions_map)

    # Add read permissions to all municipal staff types for all subresources
    add_municipal_staff_permissions(UserResourcePermission, UserType, SubResource)

# Resource-specific creation functions
def create_calendar_services(Resource, SubResource):
    calendar_resources, _ = Resource.objects.get_or_create(
        name='calendar-services',
        defaults={'description': 'Calendar and events services'}
    )

    SubResource.objects.get_or_create(
        resource=calendar_resources,
        name='events',
        defaults={
            'description': 'Calendar events sub resource services',
            'allow_anonymous': True
        }
    )

    SubResource.objects.get_or_create(
        resource=calendar_resources,
        name='comments',
        defaults={
            'description': 'Calendar comments sub resource services',
            'allow_anonymous': True
        }
    )

def create_activities_services(Resource, SubResource):
    activities_resources, _ = Resource.objects.get_or_create(
        name='activities-services',
        defaults={'description': 'Activities services'}
    )

    SubResource.objects.get_or_create(
        resource=activities_resources,
        name='fetch-activities',
        defaults={
            'description': 'Activities fetching sub resource services',
            'allow_anonymous': True
        }
    )
    SubResource.objects.get_or_create(
        resource=activities_resources,
        name='modify-activities',
        defaults={
            'description': 'Activities modifying sub resource services',
            'allow_anonymous': False
        }
    )
    SubResource.objects.get_or_create(
        resource=activities_resources,
        name='review-activities',
        defaults={
            'description': 'Activities reviewing sub resource services',
            'allow_anonymous': False
        }
    )


def create_places_services(Resource, SubResource):
    places_resources, _ = Resource.objects.get_or_create(
        name='places-services',
        defaults={'description': 'Places of interest services'}
    )

    SubResource.objects.get_or_create(
        resource=places_resources,
        name='fetch-places',
        defaults={
            'description': 'Place of interest fetching sub resource services',
            'allow_anonymous': True
        }
    )

    SubResource.objects.get_or_create(
        resource=places_resources,
        name='modify-places',
        defaults={
            'description': 'Place of interest modifying sub resource services',
            'allow_anonymous': False
        }
    )

    SubResource.objects.get_or_create(
        resource=places_resources,
        name='review-places',
        defaults={
            'description': 'Place of interest reviewing sub resource services',
            'allow_anonymous': False
        }
    )

def create_accommodation_services(Resource, SubResource):
    accommodation_resources, _ = Resource.objects.get_or_create(
        name='accommodation-services',
        defaults={'description': 'Accommodation services'}
    )

    SubResource.objects.get_or_create(
        resource=accommodation_resources,
        name='fetch-accommodation',
        defaults={
            'description': 'Accommodation fetching sub resource services',
            'allow_anonymous': True
        }
    )

    SubResource.objects.get_or_create(
        resource=accommodation_resources,
        name='modify-accommodation',
        defaults={
            'description': 'Accommodation modifying sub resource services',
            'allow_anonymous': False
        }
    )

    SubResource.objects.get_or_create(
        resource=accommodation_resources,
        name='review-accommodation',
        defaults={
            'description': 'Accommodation reviewing sub resource services',
            'allow_anonymous': False
        }
    )

def create_restaurants_services(Resource, SubResource):
    restaurants_resources, _ = Resource.objects.get_or_create(
        name='restaurants-services',
        defaults={'description': 'Restaurants services'}
    )

    SubResource.objects.get_or_create(
        resource=restaurants_resources,
        name='fetch-restaurants',
        defaults={
            'description': 'Restaurant fetching sub resource services',
            'allow_anonymous': True
        }
    )

    SubResource.objects.get_or_create(
        resource=restaurants_resources,
        name='review-restaurants',
        defaults={
            'description': 'Restaurant reviewing sub resource services',
            'allow_anonymous': False
        }
    )

def create_mapping_services(Resource, SubResource):
    mapping_resources, _ = Resource.objects.get_or_create(
        name='mapping-services',
        defaults={'description': 'Mapping services'}
    )

    SubResource.objects.get_or_create(
        resource=mapping_resources,
        name='fetch-mapping',
        defaults={
            'description': 'Mapping fetching sub resource services',
            'allow_anonymous': True
        }
    )

def create_weather_services(Resource, SubResource):
    weather_resources, _ = Resource.objects.get_or_create(
        name='weather-services',
        defaults={'description': 'Weather services'}
    )

    SubResource.objects.get_or_create(
        resource=weather_resources,
        name='fetch-weather',
        defaults={
            'description': 'Weather fetching sub resource services',
            'allow_anonymous': True
        }
    )

def create_property_services(Resource, SubResource):
    property_resources, _ = Resource.objects.get_or_create(
        name='property-services',
        defaults={'description': 'Property and land management services'}
    )

    SubResource.objects.get_or_create(
        resource=property_resources,
        name='property',
        defaults={
            'description': 'Property public sub resource services',
            'allow_anonymous': True
        }
    )

    SubResource.objects.get_or_create(
        resource=property_resources,
        name='property-admin',
        defaults={
            'description': 'Property admin sub resource services',
            'allow_anonymous': False
        }
    )

def create_health_services(Resource, SubResource):
    health_resources, _ = Resource.objects.get_or_create(
        name='health-services',
        defaults={'description': 'Health services'}
    )

    SubResource.objects.get_or_create(
        resource=health_resources,
        name='environment-health',
        defaults={
            'description': 'Environmental health sub services',
            'allow_anonymous': True
        }
    )

    SubResource.objects.get_or_create(
        resource=health_resources,
        name='modify-cemetery-health',
        defaults={
            'description': 'Cemetery health sub services',
            'allow_anonymous': False
        }
    )

    SubResource.objects.get_or_create(
        resource=health_resources,
        name='fetch-cemetery-health',
        defaults={
            'description': 'Cemetery health sub services',
            'allow_anonymous': True
        }
    )

    SubResource.objects.get_or_create(
        resource=health_resources,
        name='complaint-health',
        defaults={
            'description': 'Health complaint sub services',
            'allow_anonymous': False
        }
    )

def create_community_services(Resource, SubResource):
    community_resources, _ = Resource.objects.get_or_create(
        name='community-services',
        defaults={'description': 'Community services'}
    )

    SubResource.objects.get_or_create(
        resource=community_resources,
        name='books',
        defaults={
            'description': 'Books sub resource services',
            'allow_anonymous': True
        }
    )

    SubResource.objects.get_or_create(
        resource=community_resources,
        name='borrow',
        defaults={
            'description': 'Borrow sub resource services',
            'allow_anonymous': False
        }
    )

def create_economic_services(Resource, SubResource):
    economic_resources, _ = Resource.objects.get_or_create(
        name='economic-services',
        defaults={'description': 'Economic development services'}
    )

    SubResource.objects.get_or_create(
        resource=economic_resources,
        name='register-business',
        defaults={
            'description': 'Register business sub resource services',
            'allow_anonymous': True
        }
    )

    SubResource.objects.get_or_create(
        resource=economic_resources,
        name='modify-attraction',
        defaults={
            'description': 'Modify attraction sub resource services',
            'allow_anonymous': False
        }
    )

    SubResource.objects.get_or_create(
        resource=economic_resources,
        name='fetch-attraction',
        defaults={
            'description': 'Fetch attraction sub resource services',
            'allow_anonymous': True
        }
    )

    SubResource.objects.get_or_create(
        resource=economic_resources,
        name='modify-events',
        defaults={
            'description': 'Modify events sub resource services',
            'allow_anonymous': False
        }
    )

    SubResource.objects.get_or_create(
        resource=economic_resources,
        name='fetch-events',
        defaults={
            'description': 'Fetch events sub resource services',
            'allow_anonymous': True
        }
    )

def create_safety_services(Resource, SubResource):
    safety_resources, _ = Resource.objects.get_or_create(
        name='safety-services',
        defaults={'description': 'Public safety services'}
    )

    SubResource.objects.get_or_create(
        resource=safety_resources,
        name='report-incident',
        defaults={
            'description': 'Report incident sub resource services',
            'allow_anonymous': False
        }
    )

    SubResource.objects.get_or_create(
        resource=safety_resources,
        name='status-incident',
        defaults={
            'description': 'Status incident sub resource services',
            'allow_anonymous': True
        }
    )

def create_waste_services(Resource, SubResource):
    waste_resources, _ = Resource.objects.get_or_create(
        name='waste-services',
        defaults={'description': 'Waste management services'}
    )

    SubResource.objects.get_or_create(
        resource=waste_resources,
        name='fetch-schedule',
        defaults={
            'description': 'Fetch schedule sub resource services',
            'allow_anonymous': True
        }
    )

    SubResource.objects.get_or_create(
        resource=waste_resources,
        name='modify-schedule',
        defaults={
            'description': 'Modify schedule sub resource services',
            'allow_anonymous': False
        }
    )

    SubResource.objects.get_or_create(
        resource=waste_resources,
        name='report-pickup',
        defaults={
            'description': 'Report pickup sub resource services',
            'allow_anonymous': False
        }
    )

    SubResource.objects.get_or_create(
        resource=waste_resources,
        name='fetch-recycling',
        defaults={
            'description': 'Fetch recycling sub resource services',
            'allow_anonymous': True
        }
    )

    SubResource.objects.get_or_create(
        resource=waste_resources,
        name='modify-recycling',
        defaults={
            'description': 'Modify recycling sub resource services',
            'allow_anonymous': False
        }
    )

    SubResource.objects.get_or_create(
        resource=waste_resources,
        name='bin',
        defaults={
            'description': 'Bin sub resource services',
            'allow_anonymous': True
        }
    )

    SubResource.objects.get_or_create(
        resource=waste_resources,
        name='missed-waste-pickups',
        defaults={
            'description': 'Manage missed waste pickups sub resource services',
            'allow_anonymous': False
        }
    )

def create_citizen_portal(Resource, SubResource):
    citizen_portal, _ = Resource.objects.get_or_create(
        name='citizen-portal',
        defaults={'description': 'Citizen portal services'}
    )

    SubResource.objects.get_or_create(
        resource=citizen_portal,
        name='auth',
        defaults={
            'description': 'Citizen authentication sub resource services',
            'allow_anonymous': True
        }
    )

def create_permissions(UserResourcePermission, UserType, SubResource, permissions_map):
    for user_type_name, subresources in permissions_map.items():
        user_type = UserType.objects.get(name=user_type_name)
        for subresource_name, perms in subresources.items():
            # Get the subresource by name across all resources
            subresource = SubResource.objects.get(name=subresource_name)

            # Skip if permission already exists
            if not UserResourcePermission.objects.filter(
                user_type=user_type,
                sub_resource=subresource
            ).exists():
                UserResourcePermission.objects.create(
                    sub_resource=subresource,
                    permission=perms,
                    user_type=user_type
                )

def add_municipal_staff_permissions(UserResourcePermission, UserType, SubResource):
    municipal_staff = UserType.objects.filter(is_municipal_staff=True)
    all_subresources = SubResource.objects.all()

    for user_type in municipal_staff:
        for subresource in all_subresources:
            # Skip if already has permissions or if anonymous access is allowed
            if (not UserResourcePermission.objects.filter(
                user_type=user_type,
                sub_resource=subresource
            ).exists() and not subresource.allow_anonymous):
                UserResourcePermission.objects.create(
                    sub_resource=subresource,
                    permission=['read'],  # Basic read access to everything
                    user_type=user_type
                )                
     
        
