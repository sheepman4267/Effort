from django.test import TestCase
from django.utils import timezone

import datetime

from lists import tasks
from lists.models import TodoItem


class AutoUncheckCase(TestCase):
    def setUp(self) -> None:
        TodoItem.objects.create(
            name="recurring_with_due_date",
            completed=True,
            due_again_in=3,
        )
        TodoItem.objects.create(
            name="recurring_without_due_date",
            completed=True,
            due_again_in=None,
        )

    def test_uncheck(self):
        """Items to be unchecked which have a recurring due date get that set correctly.
        Others get no due date at all."""
        recurring_with_due_date = TodoItem.objects.get(name="recurring_with_due_date")
        recurring_without_due_date = TodoItem.objects.get(
            name="recurring_without_due_date"
        )
        tasks.uncheck_recurring_item(recurring_with_due_date.pk)
        tasks.uncheck_recurring_item(recurring_without_due_date.pk)
        recurring_with_due_date = TodoItem.objects.get(name="recurring_with_due_date")
        recurring_without_due_date = TodoItem.objects.get(
            name="recurring_without_due_date"
        )
        self.assertEqual(
            timezone.now().date()
            + datetime.timedelta(days=recurring_with_due_date.due_again_in),
            recurring_with_due_date.due_date,
        )
        self.assertEqual(None, recurring_without_due_date.due_date)
        self.assertFalse(recurring_with_due_date.completed)
        self.assertFalse(recurring_without_due_date.completed)
