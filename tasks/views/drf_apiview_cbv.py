from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models import Task, Category
from ..serializers import TaskSerializer, CategorySerializer

# An APIView calls the method named after the HTTP method (get, post, put...).
# Methods that are not defined get a 405 automatically.
# DRF turns get_object_or_404's Http404 into a 404 JSON response for us,
# and serializer.is_valid(raise_exception=True) returns a 400 with the errors.


class TaskListView(APIView):
    def get(self, request):
        tasks = Task.objects.all().order_by("-id")
        serializer = TaskSerializer(tasks, many=True)
        return Response({"count": len(serializer.data), "tasks": serializer.data})

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailView(APIView):

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        return Response(TaskSerializer(task).data)

    def put(self, request, task_id):
        return self._update(request, task_id, partial=False)

    def patch(self, request, task_id):
        return self._update(request, task_id, partial=True)

    def delete(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update(self, request, task_id, partial: bool):
        # partial=True (PATCH) means missing fields are not required
        task = get_object_or_404(Task, id=task_id)
        serializer = TaskSerializer(task, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all().order_by("-id")
        serializer = CategorySerializer(categories, many=True)
        return Response({"count": len(serializer.data), "categories": serializer.data})

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetailView(APIView):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        return Response(CategorySerializer(category).data)

    def put(self, request, category_id):
        return self._update(request, category_id, partial=False)

    def patch(self, request, category_id):
        return self._update(request, category_id, partial=True)

    def delete(self, request, category_id):
        # Note: this also deletes every task in the category (on_delete=CASCADE)
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update(self, request, category_id, partial: bool):
        category = get_object_or_404(Category, id=category_id)
        serializer = CategorySerializer(category, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
