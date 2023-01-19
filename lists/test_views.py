from django.test import TestCase
from django.test import Client
from django.shortcuts import reverse
from django.contrib.auth.models import User

from lists.models import List, ListItem


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
        self.test_list = List.objects.create(title='test_list', owner=self.user)

    def test_http_response(self) -> None:
        existing_list_response = self.client.get(reverse('list', args=[self.test_list.pk]))
        nonexisting_list_response = self.client.get(reverse('list', args=[0]))
        self.assertEqual(existing_list_response.status_code, 200)
        self.assertEqual(nonexisting_list_response.status_code, 404)
