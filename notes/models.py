from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
#from core.models import CoreContainerObject


class Folder(models.Model):
    parent = models.ForeignKey('self', unique=False, on_delete=models.CASCADE)
    pass


class Note(models.Model):
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               unique=False,
                               null=True,
                               blank=True,
                               related_name='children',
                               )
    starred = models.BooleanField(default=False)
    owner = models.ForeignKey(User,
                              unique=False,
                              on_delete=models.CASCADE,
                              related_name='notes'
                              )
    title = models.CharField(max_length=60, default='New Note')
    body = MarkdownxField()
    folder = models.ForeignKey(Folder, unique=False, on_delete=models.CASCADE, related_name='notes', null=True, blank=True)

# Create your models here.
