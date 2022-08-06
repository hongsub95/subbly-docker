from rest_framework.routers import DefaultRouter
from . import views

app_name = "users_api"
router = DefaultRouter()
router.register("", views.UserViewset)
urlpatterns = router.urls