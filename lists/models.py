from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from recurrence.fields import RecurrenceField
from markdownx.models import MarkdownxField

from django.utils import timezone

import datetime

import logging
logger = logging.getLogger('effort.lists.models')
logger.setLevel(settings.LOG_LEVEL)
print(settings.LOG_LEVEL)

class List(models.Model):
    title = models.CharField(max_length=200)
    description = MarkdownxField(blank=True)
    owner = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, unique=False, on_delete=models.CASCADE, related_name="children")
    starred = models.ManyToManyField(User, unique=False, related_name='starred')

    def __str__(self):
        return self.title

    def is_starred(self, user):
        if user in self.starred:
            return True
        else:
            return False

    def short_title(self):
        logger.debug(len(self.title))
        if len(self.title) <= 6:
            return self.title
        else:
            return f'{self.title[:5]}...'


class ListItem(models.Model):
    name = models.CharField(max_length=500)
    details = MarkdownxField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    checked_date = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    list = models.ManyToManyField(List, unique=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    uncheck_every = RecurrenceField(null=True, blank=True)
    last_unchecked = models.DateTimeField(null=True, blank=True,)
    def __str__(self):
        return(self.name)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #quick_access = models.ManyToManyField(List, related_name='quick_access')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Create your models here.
