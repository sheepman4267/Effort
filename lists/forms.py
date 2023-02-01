from django import forms
from django.db.models import fields

from markdownx.fields import MarkdownxFormField

from .models import Todo, ListItem


class ListItemForm(forms.ModelForm):
    parent_pk = forms.IntegerField(required=False)
    list_pk = forms.IntegerField(required=False)

    class Meta:
        model = ListItem
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
            instance.parent = ListItem.objects.filter(
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
        model = ListItem
        details = MarkdownxFormField
        fields = (
            "due_date",
            "current_list_pk",
            # 'uncheck_every', #Disabled due to JS bugs in django-recurrence widget
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
