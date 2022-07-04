from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from markdownx.models import MarkdownxField

import datetime

class List(models.Model):
    title = models.CharField(max_length=200)
    description = MarkdownxField(blank=True)
    owner = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, unique=False, on_delete=models.CASCADE, related_name="children")

    def __str__(self):
        return self.title

class ListItem(models.Model):
    name = MarkdownxField()
    details = MarkdownxField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(default=datetime.datetime.now, editable=False)
    completed = models.BooleanField(default=False)
    list = models.ManyToManyField(List, unique=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quick_access = models.ManyToManyField(List, related_name='quick_access')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Create your models here.
