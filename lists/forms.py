from django import forms

from markdownx.fields import MarkdownxFormField

from .models import List, ListItem

class ListItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        #name = MarkdownxFormField
        details = MarkdownxFormField
        fields = ('name',
                  'details',
                  #'list'
                  #'due_date'
                  )

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ('title',)