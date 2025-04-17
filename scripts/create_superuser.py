import os
import django
from django.core.management import call_command
from django.contrib.auth.models import User
from django.conf import settings

# Initialize Django
django.setup()

def create_superuser():
    # Read the credentials from environment variables
    username = os.getenv('SUPERUSER_USERNAME')
    email = os.getenv('SUPERUSER_EMAIL')
    password = os.getenv('SUPERUSER_PASSWORD')

    # Check if a superuser already exists
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f'Superuser {username} created successfully!')
    else:
        print(f'Superuser {username} already exists.')

if __name__ == "__main__":
    create_superuser()
