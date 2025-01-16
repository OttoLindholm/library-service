from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/book/", include("book.urls", namespace="book")),
    path("api/v1/user/", include("user.urls", namespace="user")),
    path(
        "api/v1/borrowing/", include("borrowing.urls", namespace="borrowing")
    ),
]
