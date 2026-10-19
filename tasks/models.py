from django.db import models


class Category(models.Model):
    """A group of tasks, for example "Work" or "Home"."""

    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        # This text is shown in the admin panel and in the shell
        return f"{self.id} - {self.title}"


class Task(models.Model):
    """A single to-do item."""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    completed = models.BooleanField(default=False)
    # auto_now_add sets the date only once, when the task is created
    created_at = models.DateTimeField(auto_now_add=True)
    # Each task can belong to one category (or none).
    # on_delete=CASCADE: if the category is deleted, its tasks are deleted too.
    # related_name="tasks" lets us write category.tasks.all()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.id} - {self.title}"
