from datetime import date

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from borrowing.permissions import IsOwnerOrAdmin
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


class BorrowingViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BorrowingSerializer
    queryset = Borrowing.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Borrowing.objects.all()

        if user.is_staff:
            queryset = queryset.filter(user=user)

        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            if is_active.lower() == "true":
                queryset = [b for b in queryset if b.is_active]
            elif is_active.lower() == "false":
                queryset = [b for b in queryset if not b.is_active]

        if user.is_staff:
            user_id = self.request.query_params.get("user_id")
            if user_id is not None:
                queryset = queryset.filter(user_id=user_id)

        return queryset
