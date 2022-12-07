from django import forms

from notes import models

class NewNoteForm(forms.ModelForm):

    class Meta:
        model = models.Note
        fields = ('title',)