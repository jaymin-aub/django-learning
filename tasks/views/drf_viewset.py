from rest_framework.viewsets import ModelViewSet
from ..models import Task, Category
from ..serializers import TaskSerializer, CategorySerializer

# A ModelViewSet gives every CRUD action in one class:
#   list, create, retrieve, update (PUT), partial_update (PATCH), destroy.
# A router (see tasks/urls.py) builds the URLs for it.


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all().order_by("-id")
    serializer_class = TaskSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by("-id")
    serializer_class = CategorySerializer
