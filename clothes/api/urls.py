from rest_framework.routers import DefaultRouter
from . import views

app_name = "clothes_api"
router = DefaultRouter()
router.register("", views.ClothesViewset)
urlpatterns = router.urls
