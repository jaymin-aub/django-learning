from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0002_category_task_category"),
    ]

    operations = [
        # Rename the field "Category" to "category" (lowercase, Python style)
        migrations.RenameField(
            model_name="task",
            old_name="Category",
            new_name="category",
        ),
    ]
