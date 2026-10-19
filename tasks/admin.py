from django.contrib import admin

from .models import Category, Task

# Show these models in the admin panel (/admin/)
admin.site.register(Task)
admin.site.register(Category)
