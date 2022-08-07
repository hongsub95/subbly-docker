from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from . import views

app_name = "users_api"
router = DefaultRouter()
router.register("", views.UserViewset)
router.register("/token",TokenObtainPairView.as_view(),name="token_obtain_view")
router.register("/token/refresh",TokenRefreshView.as_view(),name="token_refresh_view")
router.register("/token",TokenVerifyView.as_view(),name="token_verify_view")
urlpatterns = router.urls