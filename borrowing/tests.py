from http.client import responses

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

BORROWING_LIST_URL = reverse("borrowings:borrowing-list")


class UnauthenticatedTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_users_cannot_access(self):
        response = self.client.get(BORROWING_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
