from django import template

register = template.Library()

# 'list' is the one we're providing a button for.
# 'selected_list' is the list that is currently being displayed.
@register.inclusion_tag('lists/list-selection-display.html')
def list_selection_display(list, selected_list, request):
    if list in selected_list.tree():
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


@register.inclusion_tag('lists/star.html')
def star(request, todo):
    if request.user in todo.starred.filter():
        star_button_fill = '#ffd500'
    else:
        star_button_fill = 'transparent'
    return({
        'star_button_fill': star_button_fill,
        'todo': todo,
    })


