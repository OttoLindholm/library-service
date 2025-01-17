from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/books/", include("book.urls", namespace="books")),
    path("api/v1/users/", include("user.urls", namespace="users")),
    path(
        "api/v1/borrowings/", include("borrowing.urls", namespace="borrowings")
    ),
]
