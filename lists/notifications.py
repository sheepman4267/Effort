from django.contrib.auth import get_user_model
from django.template.defaultfilters import pluralize
from typing import List

from herald import registry
from herald.base import EmailNotification

from .models import Todo, TodoItem


class DigestEmail(EmailNotification):
    template_name = 'lists/email/digest-email'

    def __init__(self, user:get_user_model(), todo:Todo, items:List[TodoItem]):
        self.context = {
            'user': user,
            'todo': todo,
            'items': items,
        }
        self.to_emails = [user.email]

    @staticmethod
    def get_demo_args():
        user = get_user_model().objects.first()
        todo = Todo(title='Demo Todo List')
        items = TodoItem.objects.all()[:10]
        return [user, todo, items]

    def get_subject(self):
        count = len(self.context['items'])
        subject = f'{count} item{pluralize(count)} added to list "{self.context['todo']}"!'
        return subject

registry.register(DigestEmail)