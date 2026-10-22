from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..models import Task, Category
from .helpers import (
    TASK_LIST_FIELDS,
    apply_category_data,
    apply_task_data,
    category_to_dict,
    parse_json_body,
    task_to_dict,
)

# A class based View calls the method named after the HTTP method (get, post, put...).
# Methods that are not defined get a 405 Method Not Allowed automatically.
# csrf_exempt: this is a JSON API (no HTML forms), so we skip Django's CSRF check.


@method_decorator(csrf_exempt, name="dispatch")
class TaskListView(View):
    def get(self, request):
        tasks = list(Task.objects.all().order_by("-id").values(*TASK_LIST_FIELDS))
        return JsonResponse({"count": len(tasks), "tasks": tasks})

    def post(self, request):
        data, error = parse_json_body(request)
        if error:
            return JsonResponse({"error": error}, status=400)
        task = Task()
        error = apply_task_data(task, data)
        if error:
            return JsonResponse({"error": error}, status=400)
        task.save()
        return JsonResponse(task_to_dict(task), status=201)


@method_decorator(csrf_exempt, name="dispatch")
class TaskDetailView(View):
    def dispatch(self, request, task_id: int):
        # Look up the task once here, before get/put/patch/delete runs
        self.task = Task.objects.select_related("category").filter(id=task_id).first()
        if self.task is None:
            return JsonResponse({"error": "Task not found"}, status=404)
        return super().dispatch(request)

    def get(self, request):
        return JsonResponse(task_to_dict(self.task))

    def put(self, request):
        return self._update(request, partial=False)

    def patch(self, request):
        return self._update(request, partial=True)

    def delete(self, request):
        self.task.delete()
        return HttpResponse(status=204)

    def _update(self, request, partial: bool):
        data, error = parse_json_body(request)
        if error:
            return JsonResponse({"error": error}, status=400)
        error = apply_task_data(self.task, data, partial=partial)
        if error:
            return JsonResponse({"error": error}, status=400)
        self.task.save()
        return JsonResponse(task_to_dict(self.task))


@method_decorator(csrf_exempt, name="dispatch")
class CategoryListView(View):
    def get(self, request):
        categories = list(Category.objects.all().order_by("-id").values("id", "title"))
        return JsonResponse({"count": len(categories), "categories": categories})

    def post(self, request):
        data, error = parse_json_body(request)
        if error:
            return JsonResponse({"error": error}, status=400)
        category = Category()
        error = apply_category_data(category, data)
        if error:
            return JsonResponse({"error": error}, status=400)
        category.save()
        return JsonResponse(category_to_dict(category), status=201)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDetailView(View):
    def dispatch(self, request, category_id: int):
        self.category = Category.objects.filter(id=category_id).first()
        if self.category is None:
            return JsonResponse({"error": "Category not found"}, status=404)
        return super().dispatch(request)

    def get(self, request):
        return JsonResponse(category_to_dict(self.category))

    def put(self, request):
        return self._update(request, partial=False)

    def patch(self, request):
        return self._update(request, partial=True)

    def delete(self, request):
        # Note: this also deletes every task in the category (on_delete=CASCADE)
        self.category.delete()
        return HttpResponse(status=204)

    def _update(self, request, partial: bool):
        data, error = parse_json_body(request)
        if error:
            return JsonResponse({"error": error}, status=400)
        error = apply_category_data(self.category, data, partial=partial)
        if error:
            return JsonResponse({"error": error}, status=400)
        self.category.save()
        return JsonResponse(category_to_dict(self.category))
