import datetime
from django.contrib.auth.models import User
from django.db import models
from markdownx.models import MarkdownxField

import datetime

class List(models.Model):
    title = models.CharField(max_length=200)
    description = MarkdownxField(blank=True)
    owner = models.ForeignKey(User, unique=False)

class ListItem(models.Model):
    name = MarkdownxField()
    details = MarkdownxField()
    due_date = models.DateTimeField()
    created_date = models.DateTimeField(default=datetime.datetime.now(), editable=False)



# Create your models here.
