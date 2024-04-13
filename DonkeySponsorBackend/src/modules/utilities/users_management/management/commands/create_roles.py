from django.core.management.base import BaseCommand
from django.db import IntegrityError
from modules.utilities.users_management.models import Role
import os, sys
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = 'Create default roles'

    def handle(self, *args, **options):
        try:
            for role in Role.RolesInPlatform:
                try:
                    Role.objects.create(name=role[0])
                    print(f"Role {role[1]} created.")
                except IntegrityError:
                    print(f"Role {role[1]} already present.")

        except Exception as e:
            print("Something went wrong when creating the default roles")
