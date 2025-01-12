from django import template

from lists.models import Todo

from lists.forms import DetailedListItemForm

register = template.Library()


# 'list' is the one we're providing a button for.
# 'selected_list' is the list that is currently being displayed.
@register.inclusion_tag("lists/list-selection-display.html")
def list_selection_display(list, current_list, request):
    if type(current_list) != Todo:
        expand_tree = False
    elif list in current_list.tree():
        expand_tree = True
    elif list == current_list:
        expand_tree = True
    else:
        expand_tree = False
    return {
        "list": list,
        "expand_tree": expand_tree,
        "current_list": current_list,
        "request": request,
    }


@register.inclusion_tag("lists/star.html")
def star(request, todo):
    if request.user in todo.starred.filter():
        star_button_fill = "#ffd500"
    else:
        star_button_fill = "transparent"
    return {
        "star_button_fill": star_button_fill,
        "todo": todo,
    }


@register.inclusion_tag('lists/list-item-details.html')
def item_details_form(item):
    return {
        "item": item,
        "form": DetailedListItemForm(instance=item),
    }
