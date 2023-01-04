from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

app_name = "clothes_api"

urlpatterns = [
    path('',views.ClothesReadOrCreateView.as_view(),name="ClothesList_api"),
    path('<int:pk>',views.ClothesRetrieveOrDestroyView.as_view(),name = "ClothesPatchDelete_api"),
]
