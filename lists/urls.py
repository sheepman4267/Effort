from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="lists/index.html"), name="lists-index"),
    path("list/<int:pk>", views.TodoListView.as_view(), name="todo"),
    path("list/edit", views.list_edit, name="list-edit"),
    path("list/create", views.TodoListCreateView.as_view(), name="list-create"),
    path("list/edit/<int:list_pk>", views.list_edit, name="list-edit"),
    path("item/create", views.TodoItemCreateView.as_view(), name="item-create"),
    path("item/<int:pk>/update", views.TodoItemUpdateView.as_view(), name="item-update"),
    path("item/<int:pk>/details", views.ItemDetailsUpdateView.as_view(), name="item-details"),
    path("item/toggle/<int:list_pk>/<int:item>", views.toggle_item, name="toggle-item"),
    path("item/toggle-list/", views.toggle_list_on_item, name="toggle-list-on-item"),
    path("list/star/<int:todo_pk>", views.toggle_starred, name="toggle-starred"),
]
