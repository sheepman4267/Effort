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


class ListItemForm(forms.ModelForm):
    parent_pk = forms.IntegerField(required=False)
    list_pk = forms.IntegerField(required=False)

    class Meta:
        model = TodoItem
        # name = MarkdownxFormField
        name = forms.TextInput()
        fields = (
            "name",
            "parent_pk",
            "list_pk",
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

    def save(self, commit=True, *args, **kwargs):
        instance = super(ListItemForm, self).save(commit=False, *args, **kwargs)
        if not instance.parent:
            # TODO: This is why toplevel items vanish when you edit them. instance.parent gets set to instance.pk, which
            # TODO: obviously doesn't work. Rewriting this to use class based views should fix the problem, moving this
            # TODO: logic into CreateView and removing it all from EditView.
            instance.parent = TodoItem.objects.filter(
                pk=self.cleaned_data.get("parent_pk")
            ).first()
        if commit:
            instance.save()
            self.save_m2m()
        if self.cleaned_data.get("list_pk"):
            instance.list.add(Todo.objects.get(pk=self.cleaned_data.get("list_pk")))
        elif instance.parent:
            instance.list.add(
                instance.parent.list.first()
            )  # TODO: Use another field (ListItem.originating_list would be a good name) instead
        return instance


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
