# Generated by Django 4.1.5 on 2023-02-01 02:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("lists", "0004_rename_listitem_todoitem_alter_profile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todoitem",
            name="checked_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now, editable=False
            ),
        ),
    ]
