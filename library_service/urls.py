from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/books/", include("book.urls", namespace="books")),
    path("api/v1/users/", include("user.urls", namespace="users")),
    path(
        "api/v1/borrowings/", include("borrowing.urls", namespace="borrowings")
    ),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
