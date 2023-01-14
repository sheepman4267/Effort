from django import template

# from lists.models import List
# from lists.models import ListItem

register = template.Library()


# 'item' is the item we're providing a button for.
# 'selected' is the item that is currently being displayed.
@register.inclusion_tag('core/item-selection-display.html')
def item_selection_display(item, selected, request, new_item_url, new_child_item_button_text, display_url):
    if type(selected) == str:
        expand_tree = False
    elif list in get_tree(selected):
        expand_tree = True
    elif list == selected:
        expand_tree = True
    else:
        expand_tree = False
    return ({
        'item': item,
        'expand_tree': expand_tree,
        'selected': selected,
        'request': request,
        'new_item_url': new_item_url,
        'new_child_item_button_text': new_child_item_button_text,
        'display_url': display_url,
    })


# if expand_tree, htmx set whole tree visible on load, else htmx set visible on button click

# Return a list of all parents of a passed object based on core.models.CoreContainerObject
def get_tree(item):
    tree = []
    while item.parent:
        tree.append(item.parent)
        item = item.parent
    return tree


@register.inclusion_tag('lists/star.html')
def star(request, item):
    if request.user in item.starred.filter():
        star_button_text = "Unstar"
    else:
        star_button_text = "Star"
    return ({
        'star_button_text': star_button_text,
        'item': item,
    })
