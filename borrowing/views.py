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
            return queryset

        return queryset.filter(user=user)
