from django.contrib import admin
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view( 
    openapi.Info( 
        title="Swagger Study API", 
        default_version="v1", 
        description="Swagger Study를 위한 API 문서", 
        terms_of_service="https://www.google.com/policies/terms/", 
        contact=openapi.Contact(name="test", email="test@test.com"), 
        license=openapi.License(name="Test License"), 
    ), 
    public=True,  
    permission_classes=(permissions.AllowAny,), 
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("clothes/", include("clothes.urls", namespace="clothes")),
    path("users/", include("users.urls", namespace="users")),
    path("lists/", include("lists.urls", namespace="lists")),
    path("admin", admin.site.urls),
    path("orders/",include("orders.urls",namespace="orders")),
    path("api/v1/clothes/", include("clothes.api.urls", namespace="clothes_api")),
    path("api/v1/users/", include("users.api.urls", namespace="users_api")),
    path('api/v1/orders/',include('orders.api.urls',namespace='orders_api')),
]

# 이건 디버그일때만 swagger 문서가 보이도록 해주는 설정이라는 듯. urlpath도 이 안에 설정 가능해서, debug일때만 작동시킬 api도 설정할 수 있음.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

