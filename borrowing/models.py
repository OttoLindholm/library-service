from django.db import models
from django.contrib.auth import get_user_model

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrowings"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="borrowings"
    )

    def __str__(self) -> str:
        return f"{self.book.title} ({self.user.email})"
