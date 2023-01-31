import datetime

from django.shortcuts import render, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, BadRequest

from .models import Todo, ListItem
from .forms import ListForm, ListItemForm, DetailedListItemForm


@login_required
def index(request):
    starred_lists = Todo.objects.filter(
        owner=request.user,
        parent=None,
        starred=request.user,
    )
    lists = Todo.objects.filter(owner=request.user, parent=None)
    return render(
        request,
        "lists/index.html",
        {
            "starred_lists": starred_lists,
            "lists": lists,
        },
    )


@login_required
def display_list(request, list):
    list = get_object_or_404(Todo, pk=list)
    if list.owner != request.user:
        raise PermissionDenied()
    starred_lists = Todo.objects.filter(owner=request.user, starred=request.user)
    lists = Todo.objects.filter(owner=request.user, parent=None)
    return render(
        request,
        "lists/index.html",
        {
            "current_list": list,
            "lists": lists,
            "starred_lists": starred_lists,
            "todo_list_items": ListItem.objects.filter(list=list, completed=False),
            "completed_list_items": ListItem.objects.filter(
                list=list, completed=True
            ).order_by("-checked_date"),
            "quick_access": request.user.starred.filter(),
        },
    )


@login_required
def toggle_item(request, item, list_pk):
    item = ListItem.objects.get(pk=item)
    if not item.list.all() & request.user.lists.all():
        raise PermissionDenied()
    item.completed = not item.completed
    item.checked_date = datetime.datetime.now()
    item.save()
    for child_item in item.children.all():
        if item.completed and not child_item.completed:
            toggle_item(request, child_item.pk, list_pk)
    if item.parent != None:
        if (not item.completed) and item.parent.completed:
            toggle_item(request, item.parent.pk, list_pk)
    return HttpResponseRedirect(reverse("list", args=[list_pk]))


@login_required
def item_edit(request, item_pk=0):
    if request.method == "POST":
        form = ListItemForm(
            request.POST, instance=ListItem.objects.filter(pk=item_pk).first()
        )
        if form.is_valid():
            item = form.save()
            return HttpResponseRedirect(
                reverse("list", args=[item.list.filter().first().pk])
            )
    else:  # as in, if request.method != 'POST'...
        form = ListItemForm(instance=ListItem.objects.filter(pk=item_pk).first())
        return render(
            request,
            "lists/item-edit.html",
            {
                "form": form,
                "item_pk": item_pk,
            },
        )


@login_required()
def list_edit(request, list_pk=0):
    if request.method == "POST":
        existing_list = Todo.objects.filter(pk=list_pk).first()
        if existing_list and request.user != existing_list.owner:
            raise PermissionDenied()
        form = ListForm(request.POST, instance=existing_list)
        if form.is_valid():
            list = form.save()
            list.save()
            return HttpResponseRedirect(reverse("list", args=[list.pk]))
    else:  # as in, if request.method != 'POST'...
        form = ListForm(instance=Todo.objects.filter(pk=list_pk).first())
        return render(
            request,
            "lists/list-edit.html",
            {
                "form": form,
                "list_pk": list_pk,
            },
        )


@login_required()
def toggle_list_on_item(request):
    if request.method != "POST":
        raise BadRequest()
    list = get_object_or_404(Todo, pk=request.POST["list_pk"])
    item = get_object_or_404(ListItem, pk=request.POST["item_pk"])
    current_list = get_object_or_404(Todo, pk=request.POST["current_list_pk"])
    if list in item.list.all():
        item.list.remove(list)
        if len(item.list.all()) == 0:
            item.list.add(current_list)
        enabled = True
    else:
        item.list.add(list)
        enabled = False
    return render(
        request,
        "lists/quick-access-list-button.html",
        {
            "item": item,
            "list": list,
            "enabled": enabled,
        },
    )


@login_required()
def toggle_starred(request, list):
    list = Todo.objects.get(pk=list)
    if request.user in list.starred.filter():
        list.starred.remove(request.user)
        star_button_fill = "transparent"
    else:
        list.starred.add(request.user)
        star_button_fill = "#ffd500"
    list.save()
    return render(
        request,
        "lists/star.html",
        {
            "list": list,
            "star_button_fill": star_button_fill,
        },
    )


@login_required
def item_details(request, item_pk):
    item = ListItem.objects.get(pk=item_pk)
    if request.method == "POST":
        form = DetailedListItemForm(request.POST, instance=item)
        form.save()
        return HttpResponseRedirect(
            reverse("list", args=[form.cleaned_data["current_list_pk"]])
        )
    else:  # as in, if request.method != 'POST':
        form = DetailedListItemForm(instance=item)
        return render(
            request,
            "lists/list-item-details.html",
            {
                "item": item,
                "form": form,
            },
        )
