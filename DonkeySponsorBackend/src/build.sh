#!/bin/bash

echo "Applying migrations"
python manage.py makemigrations users_management
python manage.py migrate --noinput
echo "Migrations applied"


python manage.py create_roles
python manage.py create_adimin
python manage.py runserver 0.0.0.0:8000