#!/bin/bash

echo "Applying migrations"
python manage.py migrate --noinput
echo "Migrations applied"

python manage.py runserver