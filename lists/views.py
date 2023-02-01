import datetime

from django.shortcuts import render, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, BadRequest
from django.utils import timezone

from .models import Todo, TodoItem
from .forms import ListForm, ListItemForm, DetailedListItemForm


@login_required
def index(request):
    return render(request, "lists/index.html",)


@login_required
def display_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)
    if todo.owner != request.user:
        raise PermissionDenied()
    return render(
        request,
        "lists/index.html",
        {
            "current_list": todo,
        },
    )


@login_required
def toggle_item(request, item, list_pk):
    item = TodoItem.objects.get(pk=item)
    if not item.list.all() & request.user.todo_lists.all():
        raise PermissionDenied()
    item.completed = not item.completed
    item.checked_date = timezone.now()
    item.save()
    for child_item in item.children.all():
        if item.completed and not child_item.completed:
            toggle_item(request, child_item.pk, list_pk)
    if item.parent is not None:
        if (not item.completed) and item.parent.completed:
            toggle_item(request, item.parent.pk, list_pk)
    return HttpResponseRedirect(reverse("todo", args=[list_pk]))


@login_required
def item_edit(request, item_pk=0):
    if request.method == "POST":
        form = ListItemForm(
            request.POST, instance=TodoItem.objects.filter(pk=item_pk).first()
        )
        if form.is_valid():
            item = form.save()
            return HttpResponseRedirect(
                reverse("todo", args=[item.list.filter().first().pk])
            )
    else:  # as in, if request.method != 'POST'...
        form = ListItemForm(instance=TodoItem.objects.filter(pk=item_pk).first())
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
            return HttpResponseRedirect(reverse("todo", args=[list.pk]))
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
    todo = get_object_or_404(Todo, pk=request.POST["list_pk"])
    item = get_object_or_404(TodoItem, pk=request.POST["item_pk"])
    current_list = get_object_or_404(Todo, pk=request.POST["current_list_pk"])
    if todo in item.list.all():
        item.list.remove(todo)
        if len(item.list.all()) == 0:
            item.list.add(current_list)
        enabled = True
    else:
        item.list.add(todo)
        enabled = False
    return render(
        request,
        "lists/quick-access-list-button.html",
        {
            "item": item,
            "list": todo,
            "enabled": enabled,
        },
    )


@login_required()
def toggle_starred(request, todo_pk):
    todo = Todo.objects.get(pk=todo_pk)
    if request.user in todo.starred.filter():
        todo.starred.remove(request.user)
        star_button_fill = "transparent"
    else:
        todo.starred.add(request.user)
        star_button_fill = "#ffd500"
    todo.save()
    return render(
        request,
        "lists/star.html",
        {
            "todo": todo,
            "star_button_fill": star_button_fill,
        },
    )


@login_required
def item_details(request, item_pk):
    item = TodoItem.objects.get(pk=item_pk)
    if request.method == "POST":
        form = DetailedListItemForm(request.POST, instance=item)
        form.save()
        return HttpResponseRedirect(
            reverse("todo", args=[form.cleaned_data["current_list_pk"]])
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
