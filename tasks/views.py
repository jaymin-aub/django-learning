from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from .models import Category, Task
from .serializers import TaskSerializer

# Fields we send back when we list tasks.
# "category__id" means: follow the Category foreign key and take its id.
TASK_LIST_FIELDS = (
    "id",
    "title",
    "description",
    "completed",
    "created_at",
    "category__id",
    "category__title",
)


# =====================================================================
# 1. Plain Django views
#    We build the JSON ourselves and return it with JsonResponse.
# =====================================================================


def get_all_tasks(request):
    """Return a list of all tasks."""
    # .values() gives us dictionaries instead of model objects
    tasks = Task.objects.all().values(*TASK_LIST_FIELDS)
    return JsonResponse({"tasks": list(tasks)})


def get_task_details(request, task_id: int):
    """Return one task by its id. Gives a 404 error if it does not exist."""
    task = get_object_or_404(Task, id=task_id)
    return JsonResponse(
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            # A task may have no category, so we check before reading it
            "category_id": task.category.id if task.category else None,
            "category_title": task.category.title if task.category else None,
        }
    )


def get_category_with_tasks(request, category_id: int):
    """Return one category together with all of its tasks."""
    category = get_object_or_404(Category, id=category_id)
    return JsonResponse(
        {
            "id": category.id,
            "title": category.title,
            # "tasks" comes from related_name="tasks" in the Task model
            "tasks": list(category.tasks.values("id", "title", "description")),
        }
    )


# =====================================================================
# 2. DRF function views
#    @api_view tells DRF which HTTP methods are allowed.
#    Response turns Python data into JSON for us.
# =====================================================================


@api_view(["GET"])
def drf_task_list(request):
    """Same as get_all_tasks, but written with DRF."""
    tasks = Task.objects.all().values(*TASK_LIST_FIELDS)
    return Response({"tasks": list(tasks)})


@api_view(["POST"])
def create_task(request):
    """Create a new task from the JSON body of the request."""
    serializer = TaskSerializer(data=request.data)

    # The serializer checks the data before we save it
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "PATCH"])
def update_task(request, task_id: int):
    """
    Update an existing task.

    PUT   = full update (send all required fields)
    PATCH = partial update (send only the fields you want to change)
    """
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    # partial=True lets PATCH skip fields that were not sent
    partial = request.method == "PATCH"
    serializer = TaskSerializer(task, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================================================
# 3. DRF class-based (generic) views
#    DRF writes the list and create logic for us.
#    We only tell it which data to use and which serializer.
# =====================================================================


class TaskListCreateView(ListCreateAPIView):
    """GET returns all tasks, POST creates a new task."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
