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

from tasks.views import django_fbv, django_cbv, drf_apiview, drf_generic

# Namespace for these URLs, so we can refer to them as "tasks:<name>"
app_name = "tasks"

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------
    # --- Django function based views (return JsonResponse) ---
    # ------------------------------------------------------------------------------------------------------
    path("django-fbv/tasks", django_fbv.get_all_tasks, name="django_fbv_task_list"),
    path(
        "django-fbv/task/<int:task_id>",
        django_fbv.get_task_details,
        name="django_fbv_task_details",
    ),
    path(
        "django-fbv/categories",
        django_fbv.get_all_categories,
        name="django_fbv_category_list",
    ),
    # ------------------------------------------------------------------------------------------------------
    # --- Django class based views
    # ------------------------------------------------------------------------------------------------------
    path(
        "django-cbv/tasks",
        django_cbv.TaskListView.as_view(),
        name="django_cbv_task_list",
    ),
    path(
        "django-cbv/task/<int:task_id>",
        django_cbv.TaskDetailView.as_view(),
        name="django_cbv_task_details",
    ),
    path(
        "django-cbv/categories",
        django_cbv.CategoryListView.as_view(),
        name="django_cbv_category_list",
    ),
    # ------------------------------------------------------------------------------------------------------
    # --- DRF @apiview decorator based views
    # ------------------------------------------------------------------------------------------------------
    path(
        "drf-apiview/tasks",
        drf_apiview.get_all_tasks,
        name="drf_apiview_task_list",
    ),
    path(
        "drf-apiview/task/<int:task_id>",
        drf_apiview.get_task_details,
        name="drf_apiview_task_details",
    ),
    path(
        "drf-apiview/categories",
        drf_apiview.get_all_categories,
        name="drf_apiview_category_list",
    ),
    # ------------------------------------------------------------------------------------------------------
    # --- DRF generic class based views
    # ------------------------------------------------------------------------------------------------------
    path(
        "generic/tasks",
        drf_generic.TaskListCreateView.as_view(),
        name="task_list_create",
    ),
    path(
        "generic/task/<int:task_id>",
        drf_generic.TaskDetailView.as_view(),
        name="task_detail",
    ),
    path(
        "generic/categories",
        drf_generic.CategoryListCreateView.as_view(),
        name="category_list_create",
    ),
]
