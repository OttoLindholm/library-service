from django.db import transaction
from rest_framework import serializers

from borrowing.models import Borrowing
from book.models import Book
from book.serializers import BookSerializer
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
        ]

    def validate(self, data: dict):
        if data["book"].inventory <= 0:
            raise serializers.ValidationError(
                "Inventory must be greater than 0."
            )
        return data

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data["book"]
            book.inventory -= 1
            book.save()

            validated_data["user"] = self.context["request"].user
            return super().create(validated_data)


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(slug_field="title", read_only=True)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
