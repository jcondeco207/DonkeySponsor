from django.core.management.base import BaseCommand
import os, sys
from modules.utilities.users_management.models import Role, User, MustReset
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = 'Create default superuser'

    def handle(self, *args, **options):
        try:

            # Retrieve default credentials from .env file
            username = str(os.getenv('ADMIN_DEFAULT_USERNAME'))
            password = str(os.getenv('ADMIN_DEFAULT_PASSWORD'))
            email = str(os.getenv('ADMIN_DEFAULT_EMAIL'))

            # If one of the required credentials is not provided stop
            if(not username or not password or not email):
                print("Default user credentials not provided in the .env file.")
                sys.exit(1)

            adminRole = Role.objects.get(name="DonkeyAdmin")

            # Create default login
            admin = User.objects.create_superuser(username=username,
                                                  email=email,
                                                  password=password,
                                                  role=adminRole)
            admin.save()

            # Make default admin reset password on first login
            mr = MustReset.objects.create(requestedBy=admin)
            mr.save()

            print(f"Default user {username} created successfully")

        except Exception as e:
            print(e)
            sys.exit(1)
