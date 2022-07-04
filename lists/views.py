from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import List, ListItem
from .forms import ListForm, ListItemForm

@login_required
def index(request):
    lists = List.objects.filter(owner=request.user, parent=None)
    return render(request, 'lists/index.html', {
        'lists': lists,
    })

@login_required
def display_list(request, list): #TODO: No folders, just parent lists. Any list can have any number of child lists, and items can be promoted up the chain of lists.
    #list = List.objects.get(pk=list)
    list = get_object_or_404(List, pk=list)
    if list.owner != request.user:
        raise PermissionDenied()
    lists = List.objects.filter(owner=request.user, parent=None)
    #print(list.children.all())
    return render(request, 'lists/index.html', {
        'current_list': list,
        'lists': lists,
        'todo_list_items': ListItem.objects.filter(list=list, completed=False),
        'completed_list_items': ListItem.objects.filter(list=list, completed=True),
    })

@login_required
def toggle_item(request, item):
    item = ListItem.objects.get(pk=item)
    print(item.completed)
    item.completed = not item.completed
    item.save()
    print(item.completed)
    print(item.pk)
    return render(request, 'lists/list-item.html', {
        'item': item
    })

@login_required
def item_edit(request, list_pk, item=None):
    if request.method == 'POST':
        form = ListItemForm(request.POST)
        if form.is_valid():
            item = ListItem(
                name=form.cleaned_data['name'],
                details=form.cleaned_data['details'],
            )
            item.save()
            item.list.add(List.objects.get(pk=list_pk))
            return HttpResponseRedirect(reverse('list', args=[list_pk]))
        print(form.errors)
    else: #as in, if request.method != 'POST'...
        if item:
            item = ListItem.objects.get(pk=item)
            form = ListItemForm(instance=item)
        else:
            form = ListItemForm()
        return render(request, 'lists/item-edit.html', {
            'form': form,
            'list_pk': list_pk,
        })

@login_required()
def list_edit(request, list=None): #for future use, see note in list-edit.html
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            form.save()
    else: #as in, if request.method != 'POST'...
        if list:
            list = List.objects.get(pk=list)
            form = ListForm(instance=list)
        else:
            form = ListForm()
        return render(request, 'lists/list-edit.html')

@login_required()
def new_list(request, parent=None):
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            list = List(
                owner=request.user,
                title=form.cleaned_data['title'],
            )
            if parent:
                list.parent = List(pk=parent)
            list.save()
            return HttpResponseRedirect(reverse('list', args=[list.pk]))
    else: #as in, if request.method != 'POST'...
        form = ListForm()
        if parent:
            action = 'new-sublist'
        else:
            action = 'new-list'
        return render(request, 'lists/new-list.html', {
            'form': form,
            'action': action,
            'parent': parent,
        })