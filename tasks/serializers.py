"""
Serializers convert model objects to JSON (and JSON back to model objects).
They also check (validate) the incoming data.
"""

from rest_framework import serializers

from .models import Category, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"  # use every field of the model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TaskInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=500)
    description = serializers.CharField(required=False, allow_blank=True)
    completed = serializers.BooleanField(default=False)
