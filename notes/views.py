from django.shortcuts import render, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from notes.models import Note
from notes.forms import NewNoteForm
# Create your views here.


def index(request, note=None):
    if note:
        note = get_object_or_404(Note, pk=note)
    starred_notes = Note.objects.filter(starred=True, parent=None)
    notes = Note.objects.filter(starred=False, parent=None)
    return render(request, 'notes/index.html', {
        'starred': starred_notes,
        'items': notes,
        'new_item_url': 'new_note',
        'new_child_item_button_text': 'New Sub-Note',
        'note': note,
        'display_url': 'note',
    })

def new_note(request, parent=None):
    print(parent)
    print('uh')
    if request.method == 'POST':
        form = NewNoteForm(request.POST)
        if form.is_valid():
            note = Note(
                owner=request.user,
                title=form.cleaned_data['title']
            )
            if parent:
                print(parent)
                print('whyme')
                note.parent = Note(pk=int(parent))
            note.save()
            return HttpResponseRedirect(reverse('note', args=[note.pk]))
    else:  # as in, if request.method != 'POST'...
        return render(request, 'core/simple-new-item.html', {
            'form': NewNoteForm(),
            'action': 'new_note',
            'parent': parent,
        })

