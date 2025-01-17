from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from book.models import Book

BOOK_LIST_URL = reverse("book:book-list")


class UnauthenticatedTests(TestCase):
    def setUp(self):
        self.client = APIClient()
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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_update_book(self):
        data = {"title": "Updated Title"}
        response = self.client.patch(self.book_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_delete_book(self):
        response = self.client.delete(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="tes@user.com", password="password"
        )
        self.client.force_authenticate(user=self.user)

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="SOFT",
            inventory=5,
            daily_fee=1,
        )
        self.book_url = f"{BOOK_LIST_URL}{self.book.id}/"

    def test_authenticated_user_can_access_book_list(self):
        response = self.client.get(BOOK_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_cannot_create_book(self):
        data = {
            "title": "Title",
            "author": "Test Author",
            "cover": "SOFT",
            "inventory": 1,
            "daily_fee": 1,
        }
        response = self.client.post(BOOK_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cannot_update_book(self):
        data = {"title": "Updated Title"}
        response = self.client.patch(self.book_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cannot_delete_book(self):
        response = self.client.delete(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AdminUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            email="tes@admin.com", password="password"
        )
        self.client.force_authenticate(user=self.admin_user)

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="SOFT",
            inventory=5,
            daily_fee=1,
        )
        self.book_url = f"{BOOK_LIST_URL}{self.book.id}/"

    def test_admin_can_create_book(self):
        data = {
            "title": "Title",
            "author": "Test Author",
            "cover": "SOFT",
            "inventory": 1,
            "daily_fee": 1,
        }
        response = self.client.post(BOOK_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update_book(self):
        data = {"title": "Updated Title"}
        response = self.client.patch(self.book_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_book(self):
        response = self.client.delete(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

