from django.test import TestCase
from django.test import Client
from django.shortcuts import reverse
from django.contrib.auth.models import User


class IndexCase(TestCase):
    def setUp(self) -> None:
        client = Client()
        User.objects.create_user(username='test_user', password='test_password')
        client.login(username='test_user', password='test_password')
        self.index = client.get(reverse('lists-index'))

    def test_http_ok(self) -> None:
        self.assertEqual(self.index.status_code, 200)
