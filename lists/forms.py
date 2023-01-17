from django import forms
from django.db.models import fields

from markdownx.fields import MarkdownxFormField

from .models import List, ListItem


class ListItemForm(forms.ModelForm):
    parent_pk = forms.IntegerField(required=False)
    list_pk = forms.IntegerField(required=False)
    class Meta:
        model = ListItem
        # name = MarkdownxFormField
        name = forms.TextInput()
        fields = ('name',
                  'parent_pk',
                  'list_pk',
                  )
        widgets = {
            'name': forms.TextInput(attrs = {'placeholder': 'What do you need to do?',
                                             'class': 'new-item-input',
                                             'autofocus': True,
                                             'autocomplete': 'off',
                                             })
        }

    def save(self, commit=True, *args, **kwargs):
        instance = super(ListItemForm, self).save(commit=False, *args, **kwargs)
        if not instance.parent:
            instance.parent = ListItem.objects.filter(pk=self.cleaned_data.get('parent_pk')).first()
        if commit:
            instance.save()
            self.save_m2m()
        instance.list.add(List.objects.get(pk=self.cleaned_data.get('list_pk')))
        return instance

class DetailedListItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        details = MarkdownxFormField
        fields = (
            'details',
            'due_date',
            # 'uncheck_every', #Disabled due to JS bugs in django-recurrence widget
        )
        widgets = {
            'due_date': forms.DateInput(attrs = {
                'type': 'date',
            }),
        }

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ('title',)
