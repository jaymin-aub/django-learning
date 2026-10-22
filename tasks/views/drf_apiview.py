from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Task, Category
from ..serializers import TaskSerializer, CategorySerializer

# @api_view lists the allowed methods; others get a 405 automatically.
# DRF turns get_object_or_404's Http404 into a 404 JSON response for us,
# and serializer.is_valid(raise_exception=True) returns a 400 with the errors.


@api_view(["GET", "POST"])
def task_list(request):
    if request.method == "GET":
        tasks = Task.objects.all().order_by("-id")
        serializer = TaskSerializer(tasks, many=True)
        return Response({"count": len(serializer.data), "tasks": serializer.data})

    serializer = TaskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "GET":
        return Response(TaskSerializer(task).data)

    if request.method == "DELETE":
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # partial=True (PATCH) means missing fields are not required
    serializer = TaskSerializer(task, data=request.data, partial=request.method == "PATCH")
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["GET", "POST"])
def category_list(request):
    if request.method == "GET":
        categories = Category.objects.all().order_by("-id")
        serializer = CategorySerializer(categories, many=True)
        return Response({"count": len(serializer.data), "categories": serializer.data})

    serializer = CategorySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "GET":
        return Response(CategorySerializer(category).data)

    if request.method == "DELETE":
        # Note: this also deletes every task in the category (on_delete=CASCADE)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = CategorySerializer(category, data=request.data, partial=request.method == "PATCH")
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
