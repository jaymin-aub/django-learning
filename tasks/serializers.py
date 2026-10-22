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

    def validate_title(self, title: str):
        if title.isdigit():
            raise serializers.ValidationError("Title cannot contain only digits.")
        return True


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
