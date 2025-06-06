import datetime

from django.shortcuts import render, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, BadRequest
from django.utils import timezone
from django.views.generic import DetailView, CreateView, UpdateView

from .models import Todo, TodoItem
from .forms import ListForm, ListItemForm, DetailedListItemForm, CreateTodoItemForm


class TodoListView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = "lists/index.html"

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data( **kwargs)
        context["show_checked"] = bool(self.request.GET.get('showchecked', False))
        return context

    def get_object(self, queryset=None):
        todo = super().get_object()
        if todo.owner != self.request.user:
            raise PermissionDenied()
        else:
            return todo


class TodoItemCreateView(LoginRequiredMixin, CreateView):
    model = TodoItem
    form_class = CreateTodoItemForm
    template_name = 'lists/item-create.html'

    def get_success_url(self):
        return reverse('todo', kwargs={'pk': self.object.list.first().pk})


class TodoItemUpdateView(LoginRequiredMixin, UpdateView):
    model = TodoItem
    template_name = 'lists/item-update.html'
    fields = [
        'name'
    ]

    def get_success_url(self):
        return reverse('todo', kwargs={'pk': self.object.list.first().pk})


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
        "lists/list-display.html",
        {"current_list": current_list},
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


class ItemDetailsUpdateView(LoginRequiredMixin, UpdateView):
    model = TodoItem
    template_name = 'lists/list-item-details.html'
    form_class = DetailedListItemForm
    context_object_name = "item"

    def __init__(self):
        super(self.__class__).__init__()
        self.current_list_pk = None

    def form_valid(self, form):
        self.current_list_pk = form.cleaned_data[f"current_list_pk"]
        form.save()
        return self.get_success_url()

    def get_success_url(self):
        return HttpResponseRedirect(reverse("todo", args=[self.current_list_pk]))

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
