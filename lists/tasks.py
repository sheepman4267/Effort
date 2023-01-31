import datetime

from lists.models import Todo,ListItem
from django.utils import timezone

from django_q.models import Schedule


def uncheck_recurring_item(item_pk: int) -> None:
    item = ListItem.objects.get(pk=item_pk)
    item.completed = False
    if item.due_again_in:
        item.due_date = timezone.now() + datetime.timedelta(days=item.due_again_in)
    else:
        item.due_date = None
    item.save()


def collect_items(list_pk: int) -> None:
    list = Todo.objects.get(pk=list_pk)
    due_cutoff = datetime.date.today() + datetime.timedelta(days=list.collect_next_days)
    # potential_items = ListItem.objects.filter(user=list.owner, completed=False)
    potential_items = []
    for owned_list in list.owner.todo_lists.all():
        potential_items += owned_list.items.all()
    for item in potential_items:
        if item.due_date:
            if item.due_date < due_cutoff:
                item.list.add(list)
                item.save()
    Schedule.objects.create(
        func='lists.tasks.collect_items',
        args=list.pk,
        schedule_type=Schedule.ONCE,
        next_run=timezone.make_aware(datetime.datetime.combine(list.collect_on.after(datetime.datetime.now()).date(),
                                                               datetime.time(hour=0, minute=1
                                                                                    )
                                                               )
                                     )
    )

