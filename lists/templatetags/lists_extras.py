from django import template

from lists.models import List
from lists.models import ListItem

register = template.Library()

# 'list' is the one we're providing a button for.
# 'selected_list' is the list that is currently being displayed.
@register.inclusion_tag('lists/list-selection-display.html')
def list_selection_display(list, selected_list, request):
    if list in get_list_tree(selected_list):
        expand_tree = True
    elif list == selected_list:
        expand_tree = True
    else:
        expand_tree = False
    return({
        'list': list,
        'expand_tree': expand_tree,
        'selected_list': selected_list,
        'request': request,
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


@register.inclusion_tag('lists/star.html')
def star(request, list):
    if request.user in list.starred.filter():
        star_button_fill = '#ffd500'
    else:
        star_button_fill = 'transparent'
    return({
        'star_button_fill': star_button_fill,
        'list': list,
    })


