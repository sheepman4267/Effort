import datetime

from django.test import TestCase
from django.test import Client
from django.shortcuts import reverse
from django.contrib.auth.models import User

from lists.models import Todo, ListItem


class IndexCase(TestCase):
    def setUp(self) -> None:
        client = Client()
        User.objects.create_user(username='test_user', password='test_password')
        client.login(username='test_user', password='test_password')
        self.index = client.get(reverse('lists-index'))

    def test_http_response(self) -> None:
        self.assertEqual(self.index.status_code, 200)

class DisplayListCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.test_list = Todo.objects.create(title='test_list', owner=self.user)

    def test_http_response(self) -> None:
        existing_list_response = self.client.get(reverse('todo', args=[self.test_list.pk]))
        nonexisting_list_response = self.client.get(reverse('todo', args=[0]))
        self.assertEqual(existing_list_response.status_code, 200)
        self.assertEqual(nonexisting_list_response.status_code, 404)

class ToggleItemCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.other_user = User.objects.create_user(username='some_other_guy', password='another_password')
        self.client.login(username='test_user', password='test_password')
        self.test_list = Todo.objects.create(title='test_list', owner=self.user)
        self.other_guys_list = Todo.objects.create(title='I dunno what all this testing is about', owner=self.other_user)
        self.our_item = ListItem.objects.create(name='This Item is Checked', completed=False)
        self.our_item.list.add(self.test_list)
        self.other_guys_item = ListItem.objects.create(name='This Item is Unchecked', completed=False)
        self.other_guys_item.list.add(self.other_guys_list)

    def test_permissions(self) -> None:
        random_item_completed_before = self.other_guys_item.completed
        checking_random_item = self.client.get(reverse('toggle-item',
                                                       kwargs={
                                                           'item': self.other_guys_item.pk,
                                                           'list_pk': 1,
                                                       }
                                                       )) # Deliberately use bogus list_pk to make sure the function isn't using it for anything important
        self.assertEqual(checking_random_item.status_code, 403)
        self.assertEqual(random_item_completed_before, ListItem.objects.get(pk=self.other_guys_item.pk).completed)

    def test_checking_and_unchecking(self) -> None:
        our_item_completed_before = self.our_item.completed
        checking_our_item = self.client.get(reverse('toggle-item',
                                                    kwargs={
                                                        'item': self.our_item.pk,
                                                        'list_pk': 1,
                                                    }))
        self.assertNotEqual(ListItem.objects.get(pk=self.our_item.pk).completed, our_item_completed_before)
        unchecking_our_item = self.client.get(reverse('toggle-item',
                                                    kwargs={
                                                        'item': self.our_item.pk,
                                                        'list_pk': 1,
                                                    }))
        self.assertEqual(ListItem.objects.get(pk=self.our_item.pk).completed, our_item_completed_before)

    def test_http_response(self) -> None:
        checking_our_item = self.client.get(reverse('toggle-item',
                                                    kwargs={
                                                        'item': self.our_item.pk,
                                                        'list_pk': 1,
                                                    }))
        self.assertEqual(checking_our_item.status_code, 302)

class ItemEditCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.test_list = Todo.objects.create(title='test_list', owner=self.user)
        self.test_item = ListItem.objects.create(name='Test Item')
        self.test_item.list.add(self.test_list)

    def test_http_response(self) -> None:
        viewing_interface = self.client.get(reverse('item-edit',
                                                    kwargs={
                                                        'item_pk': self.test_item.pk
                                                    }))
        self.assertEqual(viewing_interface.status_code, 200)
        submitting_changes = self.client.post(reverse('item-edit',
                                                      kwargs={
                                                          'item_pk': self.test_item.pk
                                                      }
                                                      ),
                                              {
                                                  'name': 'Edited Test Item'
                                              }
                                              )
        self.assertEqual(submitting_changes.status_code, 302)

class ToggleListOnItemCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.test_list = Todo.objects.create(title='test_list', owner=self.user)
        self.test_other_list = Todo.objects.create(title='test_other_list', owner=self.user)
        self.test_item = ListItem.objects.create(name='Test Item')
        self.test_item.list.add(self.test_list)

    def test_toggle(self) -> None:
        self.client.post(reverse('toggle-list-on-item'), {
            'item_pk': self.test_item.pk,
            'list_pk': self.test_other_list.pk,
            'current_list_pk': self.test_list.pk,
        })
        self.assertIn(self.test_other_list, self.test_item.list.all())
        self.client.post(reverse('toggle-list-on-item'), {
            'item_pk': self.test_item.pk,
            'list_pk': self.test_other_list.pk,
            'current_list_pk': self.test_list.pk,
        })
        self.assertNotIn(self.test_other_list, self.test_item.list.all())


class ToggleStarredCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.test_list = Todo.objects.create(title='test_list', owner=self.user)

    def test_star_list(self):
        response = self.client.get(reverse('toggle-starred', kwargs={
            'list': self.test_list.pk
        }))
        self.assertEqual(response.context['star_button_fill'], '#ffd500')
        self.assertIn(self.user, self.test_list.starred.all())
        response = self.client.get(reverse('toggle-starred', kwargs={
            'list': self.test_list.pk
        }))
        self.assertEqual(response.context['star_button_fill'], 'transparent')
        self.assertNotIn(self.user, self.test_list.starred.all())


class ListEditCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.test_list = Todo.objects.create(title='test_list', owner=self.user)


    def test_http_response(self) -> None:
        response_new_list = self.client.get(reverse('list-edit'))
        self.assertEqual(response_new_list.status_code, 200)
        response_edit_list = self.client.get(reverse('list-edit', kwargs={
            'list_pk': self.test_list.pk
        }))
        self.assertEqual(response_edit_list.status_code, 200)

    def test_new_list(self) -> None:
        response_new_list = self.client.post(reverse('list-edit'), {
            'title': 'a completely new list!',
            'owner': self.user.pk,
            'parent': '',
        })
        self.assertEqual(response_new_list.status_code, 302)
        self.assertIsNotNone(Todo.objects.filter(title='a completely new list!').first())
        new_list = Todo.objects.get(title='a completely new list!')
        response_new_sublist = self.client.post(reverse('list-edit'), {
            'title': 'a completely new sublist!',
            'owner': self.user.pk,
            'parent': new_list.pk,
        })
        self.assertEqual(response_new_sublist.status_code, 302)
        self.assertIsNotNone(Todo.objects.filter(title='a completely new sublist!').first())
        new_sublist = Todo.objects.get(title='a completely new sublist!')
        self.assertEqual(new_sublist.parent, new_list)

    def test_edit_existing_list(self) -> None:
        new_list = Todo.objects.create(title='a toplevel list', owner=self.user)
        response_edit_toplevel = self.client.post(reverse('list-edit', args=[new_list.pk]), {
            'owner': self.user.pk,
            'title': 'a slightly different toplevel list',
        })
        self.assertEqual(response_edit_toplevel.status_code, 302)
        self.assertEqual(Todo.objects.get(pk=new_list.pk).title, 'a slightly different toplevel list')
        new_sublist = Todo.objects.create(title='a sublist', owner=self.user)
        response_edit_sublist = self.client.post(reverse('list-edit', args=[new_sublist.pk]), {
            'owner': self.user.pk,
            'title': 'a slightly different sublist',
            'parent': new_list.pk,
        })
        self.assertEqual(response_edit_sublist.status_code, 302)
        self.assertEqual(Todo.objects.get(pk=new_sublist.pk).title, 'a slightly different sublist')
        self.assertEqual(Todo.objects.get(pk=new_sublist.pk).parent, new_list)

    def test_edit_wrong_list(self) -> None:
        other_user = User.objects.create_user(username='some_other_guy', password='someone_else')
        new_list = Todo.objects.create(title='another persons list', owner=other_user)
        response_edit_wrong_list = self.client.post(reverse('list-edit', args=[new_list.pk]), {
            'owner': other_user.pk,
            'title': 'but I can change the title!',
        })
        self.assertEqual(response_edit_wrong_list.status_code, 403)
        self.assertEqual(Todo.objects.get(pk=new_list.pk).title, 'another persons list')


class ItemDetailsCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.test_list = Todo.objects.create(title='test_list', owner=self.user)
        self.test_item = ListItem.objects.create(name='test_item')
        self.test_item.list.add(self.test_list)

    def test_http_response(self) -> None:
        response_get_form = self.client.get(reverse('item-details', args=[self.test_item.pk]))
        self.assertEqual(response_get_form.status_code, 200)

    def test_post_item_changes(self) -> None:
        response_post_changes = self.client.post(reverse('item-details', args=[self.test_item.pk]), {
            'due_date': datetime.date(2023, 1, 25),
            'current_list_pk': 1,
        })
        self.assertEqual(response_post_changes.status_code, 302)
        self.assertEqual(ListItem.objects.get(pk=self.test_item.pk).due_date, datetime.date(2023, 1, 25))