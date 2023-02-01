from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from recurrence.fields import RecurrenceField
from markdownx.models import MarkdownxField

from django.utils import timezone

from django_q.models import Schedule

import datetime


class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = MarkdownxField(blank=True)
    owner = models.ForeignKey(
        User, unique=False, on_delete=models.CASCADE, related_name="todo_lists"
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        unique=False,
        on_delete=models.CASCADE,
        related_name="children",
    )
    starred = models.ManyToManyField(User, unique=False, related_name="starred")
    collect_items = models.BooleanField(default=False)
    collect_next_days = models.IntegerField(default=1)
    collect_on = RecurrenceField(null=True, blank=True)

    def checked(self):
        checked_items = self.items.filter(completed=True)
        checked_toplevel_items = checked_items.exclude(parent__in=checked_items)
        return checked_toplevel_items.order_by("-checked_date")

    def unchecked(self):
        unchecked_items = self.items.filter(completed=False)
        unchecked_toplevel_items = unchecked_items.exclude(parent__in=unchecked_items)
        return unchecked_toplevel_items

    def save(self, *args, **kwargs):
        if self.collect_items:
            Schedule.objects.create(
                func="lists.tasks.collect_items",
                args=self.pk,
                schedule_type=Schedule.ONCE,
                next_run=timezone.make_aware(
                    datetime.datetime.combine(
                        self.collect_on.after(datetime.datetime.now()).date(),
                        datetime.time(hour=0, minute=1),
                    )
                ),
            )
        super(Todo, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def is_starred(self, user):
        if user in self.starred:
            return True
        else:
            return False

    def short_title(self):
        if len(self.title) <= 6:
            return self.title
        else:
            return f"{self.title[:5]}..."

    def tree(self):
        list_tree = []
        list = self
        while list.parent:
            list_tree.append(list.parent)
            list = list.parent
        return list_tree


class ListItem(models.Model):
    name = models.CharField(max_length=500)
    details = MarkdownxField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    checked_date = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    list = models.ManyToManyField(Todo, unique=False, related_name="items")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    uncheck_every = RecurrenceField(null=True, blank=True)
    last_unchecked = models.DateTimeField(
        null=True,
        blank=True,
    )
    due_again_in = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.completed and self.uncheck_every:
            next_uncheck = self.uncheck_every.after(datetime.datetime.now())
            if next_uncheck:
                Schedule.objects.create(
                    func="lists.tasks.uncheck_recurring_item",
                    args=self.pk,
                    schedule_type=Schedule.ONCE,
                    next_run=timezone.make_aware(
                        datetime.datetime.combine(
                            next_uncheck.date() - datetime.timedelta(days=1),
                            datetime.time(hour=0, minute=1),
                        )
                    ),
                )
        super(ListItem, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def todo_lists(self):
        todo_lists = self.user.todo_lists.exclude(starred=self.user)
        toplevel_todo_lists = todo_lists.exclude(parent__in=todo_lists)
        return toplevel_todo_lists

    def starred_todo_lists(self):
        starred_todo_lists = self.user.todo_lists.filter(starred=self.user)
        toplevel_starred_todo_lists = starred_todo_lists.exclude(
            parent__in=starred_todo_lists
        )
        return toplevel_starred_todo_lists

    # quick_access = models.ManyToManyField(List, related_name='quick_access')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Create your models here.
