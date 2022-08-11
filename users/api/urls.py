from django.urls import path
from . import views


app_name = "users_api"

urlpatterns = [
    path("",views.UserViewset.as_view({'get': 'list'}),name="user_view"),
    path("token/",views.UserTokenView.as_view(),name="user_token")
]
