from django.urls import path
from . import views

app_name = "clothes"

urlpatterns = [
    path("", views.all_clothes, name="all_clothes"),
    path("clothes_list/", views.clothes_list, name="clothes_list"),
    path("int:<pk>/", views.clothes_detail.as_view(), name="clothes_detail"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("index/",views.contact_view,name="contact")
]
