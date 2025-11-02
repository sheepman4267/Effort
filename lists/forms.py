from django import forms
from django.db.models import fields

from markdownx.fields import MarkdownxFormField

from .models import Todo, TodoItem


class CreateTodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        name = forms.TextInput()
        fields = (
            "name",
            "parent",
            "list",
            "originating_todo",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "What do you need to do?",
                    "class": "new-item-input",
                    "autofocus": True,
                    "autocomplete": "off",
                }
            )
        }


class DetailedListItemForm(forms.ModelForm):
    current_list_pk = forms.IntegerField(required=False)

    class Meta:
        model = TodoItem
        details = MarkdownxFormField
        fields = (
            "due_date",
            "current_list_pk",
            'uncheck_every',
        )
        widgets = {
            "due_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }


class ListForm(forms.ModelForm):
    # parent_pk = forms.IntegerField(required=False)
    class Meta:
        model = Todo
        fields = (
            "title",
            "owner",
            "parent",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={
                    'autofocus': True,
                }
            )
        }
