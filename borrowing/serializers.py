from rest_framework import serializers

from borrowing.models import Borrowing
from book.models import Book
from book.serializers import BookSerializer
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]

    def validate(self, data: dict):
        if data["book"].inventory <= 0:
            raise serializers.ValidationError("Inventory must be greater than 0.")


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(slug_field="title", read_only=True)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
