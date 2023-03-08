from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path("clothes/", include("clothes.urls", namespace="clothes")),
    path("users/", include("users.urls", namespace="users")),
    path("lists/", include("lists.urls", namespace="lists")),
    path("admin", admin.site.urls),
    path("orders/",include("orders.urls",namespace="orders")),
    path("api/v1/clothes/", include("clothes.api.urls", namespace="clothes_api")),
    path("api/v1/users/", include("users.api.urls", namespace="users_api")),
    path('api/v1/orders/',include('orders.api.urls',namespace='orders_api')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
