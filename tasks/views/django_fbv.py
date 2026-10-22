from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..models import Task, Category
from .helpers import (
    TASK_LIST_FIELDS,
    apply_category_data,
    apply_task_data,
    category_to_dict,
    parse_json_body,
    task_to_dict,
)

# csrf_exempt: this is a JSON API (no HTML forms), so we skip Django's CSRF check.
# require_http_methods: any other method gets a 405 Method Not Allowed.


# ------------------------------------------------------------------------------
# Tasks
# ------------------------------------------------------------------------------
@csrf_exempt
@require_http_methods(["GET", "POST"])
def task_list(request):
    # GET -> list all tasks
    if request.method == "GET":
        tasks = list(Task.objects.all().order_by("-id").values(*TASK_LIST_FIELDS))
        return JsonResponse({"count": len(tasks), "tasks": tasks})

    # POST -> create a task
    data, error = parse_json_body(request)
    if error:
        return JsonResponse({"error": error}, status=400)
    task = Task()
    error = apply_task_data(task, data)
    if error:
        return JsonResponse({"error": error}, status=400)
    task.save()
    return JsonResponse(task_to_dict(task), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def task_detail(request, task_id: int):
    task = Task.objects.select_related("category").filter(id=task_id).first()
    if task is None:
        return JsonResponse({"error": "Task not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(task_to_dict(task))

    if request.method == "DELETE":
        task.delete()
        return HttpResponse(status=204)

    # PUT replaces every field, PATCH only changes the fields that are sent
    data, error = parse_json_body(request)
    if error:
        return JsonResponse({"error": error}, status=400)
    error = apply_task_data(task, data, partial=request.method == "PATCH")
    if error:
        return JsonResponse({"error": error}, status=400)
    task.save()
    return JsonResponse(task_to_dict(task))


# ------------------------------------------------------------------------------
# Categories
# ------------------------------------------------------------------------------
@csrf_exempt
@require_http_methods(["GET", "POST"])
def category_list(request):
    if request.method == "GET":
        categories = list(Category.objects.all().order_by("-id").values("id", "title"))
        return JsonResponse({"count": len(categories), "categories": categories})

    data, error = parse_json_body(request)
    if error:
        return JsonResponse({"error": error}, status=400)
    category = Category()
    error = apply_category_data(category, data)
    if error:
        return JsonResponse({"error": error}, status=400)
    category.save()
    return JsonResponse(category_to_dict(category), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def category_detail(request, category_id: int):
    category = Category.objects.filter(id=category_id).first()
    if category is None:
        return JsonResponse({"error": "Category not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(category_to_dict(category))

    if request.method == "DELETE":
        # Note: this also deletes every task in the category (on_delete=CASCADE)
        category.delete()
        return HttpResponse(status=204)

    data, error = parse_json_body(request)
    if error:
        return JsonResponse({"error": error}, status=400)
    error = apply_category_data(category, data, partial=request.method == "PATCH")
    if error:
        return JsonResponse({"error": error}, status=400)
    category.save()
    return JsonResponse(category_to_dict(category))
