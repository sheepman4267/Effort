from django.db import models
from django.contrib.auth.models import User
from django.urls.base import reverse


# class CoreContainerObject(models.Model):
#     parent = models.ForeignKey('self',
#                                on_delete=models.CASCADE,
#                                unique=False,
#                                null=True,
#                                blank=True,
#                                related_name='children',
#                                )
#     starred = models.BooleanField(default=False)
#     owner = models.ForeignKey(User,
#                               unique=False,
#                               on_delete=models.CASCADE,
#                               related_name='notes'
#                               )


class Category(models.Model):
    # A Category which can be linked to by other models. This is mostly for reporting right now.
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('core-category-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
