"""
Main URL file for the whole project.

Django reads this file first when a request comes in.
Each app keeps its own urls.py, and we connect it here with include().
"""

from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    # GET health/ -> simple check to see if the server is running
    path("health/", views.health, name="health_check"),
    # Built-in Django admin panel
    path("admin/", admin.site.urls),
    # All task URLs live in tasks/urls.py and start with "api/tasks/"
    path("api/tasks/", include("tasks.urls")),
]
