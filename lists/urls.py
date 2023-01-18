from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='lists-index'),
    path('list/<int:list>', views.display_list, name='list'),
    path('list/new', views.new_list, name='new-list'),
    path('list/new/<int:parent>', views.new_list, name='new-sublist'),
    path('item/edit', views.item_edit, name='item-edit'),
    path('item/edit/<int:item_pk>', views.item_edit, name='item-edit'),
    path('item/<int:item_pk>/details', views.item_details, name='item-details'),
    path('item/toggle/<int:list_pk>/<int:item>', views.toggle_item, name='toggle-item'),
    path('item/<int:current_list>/<int:item>/add/<int:list>', views.add_item_to_list, name='add-item-to-list'),
    path('item/<int:current_list>/<int:item>/remove/<int:list>', views.remove_item_from_list, name='remove-item-from-list'),
    path('list/star/<int:list>', views.toggle_starred, name='toggle-starred'),
]