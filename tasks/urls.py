"""
URLs for the tasks app.

Every path here starts with "api/tasks/" (see task_manager/urls.py).
For example, "generic/tasks" below becomes "api/tasks/generic/tasks".

The same CRUD API is built in several styles, one URL prefix per style:
    django-fbv/   -> plain Django function views (JsonResponse)
    django-cbv/   -> plain Django class based views
    drf-apiview/  -> DRF @api_view function views
    generic/      -> DRF generic class based views
    viewset/      -> DRF ModelViewSet + router

Each style (except viewset, whose URLs come from the router) has:
    <style>/tasks                       GET (list), POST (create)
    <style>/task/<task_id>              GET, PUT, PATCH, DELETE
    <style>/categories                  GET (list), POST (create)
    <style>/category/<category_id>      GET, PUT, PATCH, DELETE
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from tasks.views import django_fbv, django_cbv, drf_apiview, drf_generic, drf_viewset

# Namespace for these URLs, so we can refer to them as "tasks:<name>"
app_name = "tasks"

urlpatterns = [
    # ------------------------------------------------------------------------------------------------------
    # --- Django function based views (return JsonResponse) ---
    # ------------------------------------------------------------------------------------------------------
    path("django-fbv/tasks", django_fbv.task_list, name="django_fbv_task_list"),
    path(
        "django-fbv/task/<int:task_id>",
        django_fbv.task_detail,
        name="django_fbv_task_details",
    ),
    path(
        "django-fbv/categories",
        django_fbv.category_list,
        name="django_fbv_category_list",
    ),
    path(
        "django-fbv/category/<int:category_id>",
        django_fbv.category_detail,
        name="django_fbv_category_details",
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
    path(
        "django-cbv/category/<int:category_id>",
        django_cbv.CategoryDetailView.as_view(),
        name="django_cbv_category_details",
    ),
    # ------------------------------------------------------------------------------------------------------
    # --- DRF @apiview decorator based views
    # ------------------------------------------------------------------------------------------------------
    path(
        "drf-apiview/tasks",
        drf_apiview.task_list,
        name="drf_apiview_task_list",
    ),
    path(
        "drf-apiview/task/<int:task_id>",
        drf_apiview.task_detail,
        name="drf_apiview_task_details",
    ),
    path(
        "drf-apiview/categories",
        drf_apiview.category_list,
        name="drf_apiview_category_list",
    ),
    path(
        "drf-apiview/category/<int:category_id>",
        drf_apiview.category_detail,
        name="drf_apiview_category_details",
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
    path(
        "generic/category/<int:category_id>",
        drf_generic.CategoryDetailView.as_view(),
        name="category_detail",
    ),
]

# ------------------------------------------------------------------------------------------------------
# --- DRF viewsets: the router creates the URLs for us
#     viewset/tasks, viewset/tasks/<pk>, viewset/categories, viewset/categories/<pk>
# ------------------------------------------------------------------------------------------------------
router = DefaultRouter(trailing_slash=False)
router.register("viewset/tasks", drf_viewset.TaskViewSet, basename="viewset_task")
router.register("viewset/categories", drf_viewset.CategoryViewSet, basename="viewset_category")
urlpatterns += router.urls
