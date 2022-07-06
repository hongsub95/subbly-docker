from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("clothes/", include("clothes.urls", namespace="clothes")),
    path("users/", include("users.urls", namespace="users")),
    path("lists/", include("lists.urls", namespace="lists")),
    path("admin", admin.site.urls),
    path("api/v1/clothes/", include("clothes.api.urls", namespace="clothes_api")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
