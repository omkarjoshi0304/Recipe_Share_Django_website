#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate

echo " Adding default Item Categories..."
python manage.py shell << END
from main.models import ItemCategory
default_categories = ["Utensils", "Appliances", "Cookware", "Storage", "Cutlery"]
for name in default_categories:
    ItemCategory.objects.get_or_create(name=name)
END

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
