import os
import django

# Set Django settings module configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

print("Starting automated deployment database setup...")

try:
    print("Running database migrations...")
    call_command('migrate', interactive=False)
    print("Migrations complete.")
    
    # Pull credentials from environment variables or default to admin/admin123
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    email = 'admin@example.com'

    if not User.objects.filter(username=username).exists():
        print(f"Seeding superuser: {username}...")
        User.objects.create_superuser(username, email, password)
        print("Superuser created successfully.")
    else:
        print(f"Superuser {username} already exists. Updating password...")
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
        print("Superuser password updated successfully.")
except Exception as e:
    print(f"Warning: Database connection deferred during build phase: {e}")

print("Deployment build setup complete.")
