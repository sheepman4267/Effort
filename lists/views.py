import datetime

from django.shortcuts import render, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import List, ListItem
from .forms import ListForm, ListItemForm, DetailedListItemForm

@login_required
def index(request):
    starred_lists = List.objects.filter(owner=request.user, parent=None, starred=request.user)
    lists = List.objects.filter(owner=request.user, parent=None)
    return render(request, 'lists/index.html', {
        'starred_lists': starred_lists,
        'lists': lists,
    })

@login_required
def display_list(request, list): #TODO: No folders, just parent lists. Any list can have any number of child lists, and items can be promoted up the chain of lists.
    list = get_object_or_404(List, pk=list)
    if list.owner != request.user:
        raise PermissionDenied()
    starred_lists = List.objects.filter(owner=request.user, starred=request.user)
    lists = List.objects.filter(owner=request.user, parent=None)
    return render(request, 'lists/index.html', {
        'current_list': list,
        'lists': lists,
        'starred_lists': starred_lists,
        'todo_list_items': ListItem.objects.filter(list=list, completed=False),
        'completed_list_items': ListItem.objects.filter(list=list, completed=True).order_by("-checked_date"),
        'quick_access': request.user.starred.filter()
    })

@login_required
def toggle_item(request, item, list_pk):
    if not item.list.all() & request.user.lists.all():
        raise PermissionDenied()
    item = ListItem.objects.get(pk=item)
    item.completed = not item.completed
    item.checked_date = datetime.datetime.now()
    item.save()
    for child_item in item.children.all():
        if item.completed and not child_item.completed:
            toggle_item(request, child_item.pk, list_pk)
    if item.parent != None:
         if (not item.completed) and item.parent.completed:
            toggle_item(request, item.parent.pk, list_pk)
    return HttpResponseRedirect(reverse('list', args=[list_pk]))

@login_required
def item_edit(request, item_pk=0):
    if request.method == 'POST':
        form = ListItemForm(request.POST, instance=ListItem.objects.filter(pk=item_pk).first())
        if form.is_valid():
            item = form.save()
            return HttpResponseRedirect(reverse('list', args=[item.list.filter().first().pk]))
    else: #as in, if request.method != 'POST'...
        form = ListItemForm(instance=ListItem.objects.filter(pk=item_pk).first())
        return render(request, 'lists/item-edit.html', {
            'form': form,
            'item_pk': item_pk,
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
def add_item_to_list(request, item, list, current_list):
    item = ListItem.objects.get(pk=item)
    list = List.objects.get(pk=list)
    item.list.add(list)
    item.save()
    return render(request, 'lists/quick-access-list-button.html', {
        'item': item,
        'list': list,
        'enabled': False,
        'current_list': current_list,
    })

@login_required()
def remove_item_from_list(request, item, list, current_list):
    current_list = List.objects.get(pk=current_list)
    item = ListItem.objects.get(pk=item)
    list = List.objects.get(pk=list)
    item.list.remove(list)
    if len(item.list.all()) == 0:
        item.list.add(current_list)
    item.save()
    return render(request, 'lists/quick-access-list-button.html', {
        'item': item,
        'list': list,
        'enabled': True,
        'current_list': current_list.pk
    })

@login_required()
def toggle_starred(request, list):
    list = List.objects.get(pk=list)
    if request.user in list.starred.filter():
        list.starred.remove(request.user)
        star_button_fill = 'transparent'
    else:
        list.starred.add(request.user)
        star_button_fill = '#ffd500'
    list.save()
    return render(request, 'lists/star.html', {
        'list': list,
        'star_button_fill': star_button_fill,
    })

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
                list.parent = List.objects.get(pk=parent)
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

@login_required
def item_details(request, item_pk):
    item = ListItem.objects.get(pk=item_pk)
    if request.method == 'POST':
        form = DetailedListItemForm(request.POST, instance=item)
        form.save()
        return HttpResponseRedirect(reverse('list', args=[1]))
    else: # as in, if request.method != 'POST':
        form = DetailedListItemForm(instance=item)
        return render(request, 'lists/list-item-details.html', {
            'item': item,
            'form': form,
        })
