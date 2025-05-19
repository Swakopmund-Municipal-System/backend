#!/bin/bash

# Apply database migrations
python manage.py migrate

python manage.py collectstatic --noinput --clear

# Create superuser (if not exists)
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
# The import path needs to be corrected - let's locate UserType
# Based on your model structure, UserType seems to be in the same app as User
from django.apps import apps

User = get_user_model()
# Find the app that contains UserType
user_app = User._meta.app_label
UserType = apps.get_model(user_app, 'UserType')

email = '$DJANGO_SUPERUSER_EMAIL'
password = '$DJANGO_SUPERUSER_PASSWORD'
is_staff = '${DJANGO_SUPERUSER_IS_STAFF:-False}'

print(f"Attempting to create superuser with email: {email}")

if not User.objects.filter(email=email).exists():
    print(f"Creating superuser with email: {email}")
    superuser = User.objects.create_superuser(
        email=email,
        password=password,
        is_staff=True,
        is_superuser=True
    )
    
    # Add municipal staff status
    if is_staff.lower() == 'true':
        print("Adding Administrator user type")
        try:
            staff_type, created = UserType.objects.get_or_create(
                name='Administrator',
                is_municipal_staff=True
            )
            superuser.user_types.add(staff_type)
            superuser.save()
            print("Successfully added staff type to superuser")
        except Exception as e:
            print(f"Error adding user type: {str(e)}")
    print("Superuser created successfully!")
else:
    print(f"Superuser with email {email} already exists")
EOF

# Start server
exec "$@"
