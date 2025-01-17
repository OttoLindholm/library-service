from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from book.models import Book
from borrowing.models import Borrowing


BORROWING_LIST_URL = reverse("borrowings:borrowing-list")


def sample_book(**params):
    defaults = {
        "title": "Sample Title",
        "author": "Sample Author",
        "cover": "SOFT",
        "inventory": 1,
        "daily_fee": 1,
    }
    defaults.update(params)
    return Book.objects.create(**defaults)

def sample_borrowing(user, book, borrow_date, expected_return_date, is_active=True):
    return Borrowing.objects.create(
        user=user,
        book=book,
        borrow_date=borrow_date,
        expected_return_date=expected_return_date,
        is_active=is_active,)


class UnauthenticatedTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_users_cannot_access(self):
        response = self.client.get(BORROWING_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="tes@user.com", password="password"
        )
        self.client.force_authenticate(user=self.user)

    def test_can_create_borrowing(self):
        data = {
            "borrow_date": date(25, 1, 15),
            "expected_return_date": date(25, 1, 16),
            "book": sample_book().id,
        }
        response = self.client.post(BORROWING_LIST_URL, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 1)

        borrowing = Borrowing.objects.first()

        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(borrowing.book.inventory, 0)

class BorrowingFilterAndPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="password123",
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="adminpass",
        )
        self.client.force_authenticate(self.user)
        self.book = sample_book()

    def test_filter_is_active(self):
        active_borrowing = sample_borrowing(
            user=self.user,
            book=self.book,
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
            is_active=True,
        )
        inactive_borrowing = sample_borrowing(
            user=self.user,
            book=self.book,
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
            is_active=False,
        )

        response = self.client.get(BORROWING_LIST_URL, {"is_active": "true"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], active_borrowing.id)

        response = self.client.get(BORROWING_LIST_URL, {"is_active": "false"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], inactive_borrowing.id)
