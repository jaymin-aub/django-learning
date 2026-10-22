from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from ..models import Task, Category


class TaskListView(View):
    TASK_LIST_FIELDS = (
        "id",
        "title",
        "description",
        "completed",
        "created_at",
        "category__id",
        "category__title",
    )

    def get(self, request):
        tasks = Task.objects.all().order_by("-id").values(*self.TASK_LIST_FIELDS)
        task_list = list(tasks)

        return JsonResponse(
            {
                "count": len(task_list),
                "tasks": task_list,
            }
        )


class TaskDetailView(View):
    def get(self, request, task_id: int):
        try:
            task = get_object_or_404(Task, id=task_id)
        except Http404:
            return JsonResponse({"error": "Task not found"}, status=404)
        return JsonResponse(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "category_id": task.category.id if task.category else None,
                "category_title": task.category.title if task.category else None,
            }
        )


class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all().order_by("-id").values("id", "title")
        category_list = list(categories)

        return JsonResponse(
            {
                "count": len(category_list),
                "categories": category_list,
            }
        )
