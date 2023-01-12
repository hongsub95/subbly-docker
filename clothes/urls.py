from django.urls import path
from . import views

app_name = "clothes"

urlpatterns = [
    path("", views.all_clothes, name="all_clothes"),
    path('clothes_list',views.clothes_list,name="clothes_list"),
    path("upper/", views.clothes_list_upper, name="clothes_list_upper"),
    path("pants/", views.clothes_list_pants, name="clothes_list_pants"),
    path("shoes/", views.clothes_list_shoes, name="clothes_list_shoes"),
    path("outer/", views.clothes_list_outer, name="clothes_list_outer"),
    path("onepiece/", views.clothes_list_onepiece, name="clothes_list_onepiece"),
    path("int:<pk>/", views.clothes_detail.as_view(), name="clothes_detail"),
    path("search/", views.SearchView.as_view(), name="search"),
   
]