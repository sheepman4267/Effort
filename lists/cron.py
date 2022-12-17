import datetime
from django.utils import timezone

from lists import models


def uncheck_recurring_items():
    recurring_items = models.ListItem.objects.filter(completed=True, uncheck_every__isnull=False)
    for item in recurring_items:
        uncheck_next = timezone.make_aware(item.uncheck_every.after(datetime.datetime.now()))
        if uncheck_next and (timezone.now() - uncheck_next) <= datetime.timedelta(days=1):
            print(f'last unchecked {item.last_unchecked}')
            print(f'uncheck next {uncheck_next}')
            if item.last_unchecked != uncheck_next:
                item.completed = False
                item.last_unchecked = uncheck_next
                item.save()
                print('unchecked an item!')