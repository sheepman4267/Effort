from django.db import models
from django.contrib.auth.models import User

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


