"""
Small helpers shared by the plain Django views (django_fbv.py and django_cbv.py).

Plain Django has no serializers, so we turn models into dicts and check the
incoming JSON by hand here. The DRF views use tasks/serializers.py instead.
"""

import json

from ..models import Category, Task

TASK_LIST_FIELDS = (
    "id",
    "title",
    "description",
    "completed",
    "created_at",
    "category__id",
    "category__title",
)


def task_to_dict(task: Task) -> dict:
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at.isoformat(),
        "category_id": task.category.id if task.category else None,
        "category_title": task.category.title if task.category else None,
    }


def category_to_dict(category: Category) -> dict:
    return {"id": category.id, "title": category.title}


def parse_json_body(request):
    """Return (data, error). data is a dict when the body is valid JSON."""
    try:
        data = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return None, "Request body must be valid JSON."
    if not isinstance(data, dict):
        return None, "Request body must be a JSON object."
    return data, None


def validate_title(data: dict, partial: bool):
    """Return an error message, or None when the title is fine."""
    if "title" not in data:
        return None if partial else "Title is required."
    title = data["title"]
    if not isinstance(title, str) or not title.strip():
        return "Title must be a non-empty string."
    if len(title) > 255:
        return "Title must be at most 255 characters."
    return None


def apply_task_data(task: Task, data: dict, partial: bool = False):
    """
    Copy fields from data onto task (does not save).
    partial=True is used for PATCH: missing fields are left unchanged.
    Returns an error message, or None when everything is valid.
    """
    error = validate_title(data, partial)
    if error:
        return error
    if "title" in data:
        if data["title"].isdigit():
            return "Title cannot contain only digits."
        task.title = data["title"]

    if "description" in data or not partial:
        description = data.get("description", "")
        if not isinstance(description, str):
            return "Description must be a string."
        task.description = description

    if "completed" in data or not partial:
        completed = data.get("completed", False)
        if not isinstance(completed, bool):
            return "Completed must be true or false."
        task.completed = completed

    if "category" in data or not partial:
        category_id = data.get("category")
        if category_id is None:
            task.category = None
        else:
            category = Category.objects.filter(id=category_id).first()
            if category is None:
                return f"Category {category_id} does not exist."
            task.category = category
    return None


def apply_category_data(category: Category, data: dict, partial: bool = False):
    """Same idea as apply_task_data, for categories."""
    error = validate_title(data, partial)
    if error:
        return error
    if "title" in data:
        category.title = data["title"]
    return None
