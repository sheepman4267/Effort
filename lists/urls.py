from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/<int:list>', views.display_list, name='list'),
    path('list/new', views.new_list, name='new-list'),
    path('list/new/<int:parent>', views.new_list, name='new-sublist'),
    path('item/edit/<int:list_pk>/new', views.item_edit, name='new-item'),
    path('item/edit/<int:list_pk>/<int:item>', views.item_edit, name='edit-item'),
    path('item/toggle/<int:item>', views.toggle_item, name='toggle-item'),
    path('item/<int:item>/add/<int:list>', views.add_item_to_list, name='add-item-to-list'),
    path('list/star/<int:list>', views.toggle_starred, name='toggle-starred')
]