"""
URLs for the tasks app.

Every path here starts with "api/tasks/" (see task_manager/urls.py).
For example, "drf/create/" below becomes "api/tasks/drf/create/".

The URLs are grouped by the style of view they use:
    api/tasks/...           -> plain Django views
    api/tasks/drf/...       -> DRF function views
    api/tasks/generic/      -> DRF class-based (generic) view
"""

from django.urls import path

from . import views

# Namespace for these URLs, so we can refer to them as "tasks:<name>"
app_name = "tasks"

urlpatterns = [
    # --- Plain Django views (return JsonResponse) ---
    # GET  api/tasks/                     -> list all tasks
    path("", views.get_all_tasks, name="task_list"),
    # GET  api/tasks/5/                   -> details of task 5
    path("<int:task_id>/", views.get_task_details, name="task_detail"),
    # GET  api/tasks/category/2/          -> category 2 with its tasks
    path(
        "category/<int:category_id>/",
        views.get_category_with_tasks,
        name="category_tasks",
    ),
    # --- DRF function views (use @api_view and Response) ---
    # GET  api/tasks/drf/                 -> list all tasks
    path("drf/", views.drf_task_list, name="drf_task_list"),
    # POST api/tasks/drf/create/          -> create a new task
    path("drf/create/", views.create_task, name="drf_task_create"),
    # PUT or PATCH api/tasks/drf/5/update/ -> update task 5
    path("drf/<int:task_id>/update/", views.update_task, name="drf_task_update"),
    # --- DRF class-based view ---
    # GET  api/tasks/generic/             -> list all tasks
    # POST api/tasks/generic/             -> create a new task
    path("generic/", views.TaskListCreateView.as_view(), name="generic_task_list_create"),
]
