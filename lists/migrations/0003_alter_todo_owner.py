# Generated by Django 4.1.5 on 2023-01-31 02:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("lists", "0002_rename_list_todo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todo",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="todo_lists",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
