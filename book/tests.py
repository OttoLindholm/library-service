from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from book.models import Book

BOOK_LIST_URL = reverse("book:book-list")


class UnauthenticatedTests(TestCase):
    def setUp(self):
        client = APIClient()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="SOFT",
            inventory=5,
            daily_fee=1,
        )
        self.book_url = f"{BOOK_LIST_URL}{self.book.id}/"

    def test_can_access_book_list(self):
        response = self.client.get(BOOK_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_create_book(self):
        data = {
            "title": "Title",
            "author": "Test Author",
            "cover": "SOFT",
            "inventory": 1,
            "daily_fee": 1,
        }
        response = self.client.post(
            BOOK_LIST_URL,
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_update_book(self):
        data = {"title": "Updated Title"}
        response = self.client.patch(self.book_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_delete_book(self):
        response = self.client.delete(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
