from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..models import Task, Category
from ..serializers import TaskSerializer, CategorySerializer

# ListCreateAPIView            -> GET (list) and POST (create)
# RetrieveUpdateDestroyAPIView -> GET (one), PUT, PATCH and DELETE


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all().order_by("-id")
    serializer_class = TaskSerializer


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_url_kwarg = "task_id"


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all().order_by("-id")
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = "category_id"
