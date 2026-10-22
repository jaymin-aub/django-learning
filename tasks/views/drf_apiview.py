from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Task, Category

from django.http import Http404
from django.shortcuts import get_object_or_404

# from ..serializers import TaskSerializer, CategorySerializer

TASK_LIST_FIELDS = (
    "id",
    "title",
    "description",
    "completed",
    "created_at",
    "category__id",
    "category__title",
)


@api_view(["GET"])
def get_all_tasks(request):
    tasks = Task.objects.all().values(*TASK_LIST_FIELDS).order_by("-id")
    task_list = list(tasks)
    return Response(
        {
            "count": len(task_list),
            "tasks": task_list,
        }
    )


@api_view(["GET"])
def get_task_details(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id)
    except Http404:
        return Response({"error": "Task not found"}, status=404)
    return Response(
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


@api_view(["GET"])
def get_all_categories(request):
    categories = Category.objects.all().values("id", "title").order_by("id")
    return Response({"count": len(categories), "categories": categories})
