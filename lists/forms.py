from django import forms

from markdownx.fields import MarkdownxFormField

from .models import List, ListItem


class ListItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        # name = MarkdownxFormField
        name = forms.TextInput()
        fields = ('name',
                  # 'details',
                  # 'list'
                  # 'due_date'
                  )
        widgets = {
            'name': forms.TextInput(attrs = {'placeholder': 'What do you need to do?',
                                             'class': 'new-item-input',
                                             'autofocus': True,
                                             'autocomplete': 'off',
                                             })
        }

class DetailedListItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        details = MarkdownxFormField
        fields = ('name',
                  'details',
                  'due_date',
        )

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ('title',)
