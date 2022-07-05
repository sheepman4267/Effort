from django import template

from lists.models import List
from lists.models import ListItem

register = template.Library()

# 'list' is the one we're providing a button for.
# 'selected_list' is the list that is currently being displayed.
@register.inclusion_tag('lists/list-selection-display.html')
def list_selection_display(list, selected_list, request):
    if len(list.children.all()) > 0:
        list_has_children = True
    else:
        list_has_children = False
    if list in get_list_tree(selected_list):
        print('itsthere')
        expand_tree = True
    elif list == selected_list:
        expand_tree = True
    else:
        expand_tree = False
    return({
        'list': list,
        'expand_tree': expand_tree,
        'selected_list': selected_list,
        'list_has_children': list_has_children,
    })

#if expand_tree, htmx set whole tree visible on load, else htmx set visible on button click

#Return a list of all parents of a passed List object
def get_list_tree(list):
    list_tree = []
    if type(list) != List:
        return [] #this is awful, but should work
    while list.parent:
        list_tree.append(list.parent)
        list = list.parent
    return list_tree