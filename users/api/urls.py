from django.urls import path
from . import views


app_name = "users_api"

urlpatterns = [
    path("",views.UserViewset.as_view({'get': 'list'}),name="user_view"),
    #path("register/",views.RegisterAPIView.as_view(),name="user_register"),
    path("token/",views.UserTokenView.as_view(),name="user_token"),
    path("token/refresh/refresh_token/",views.UserRefreshTokenView.as_view(),name="user_refresh_token")
]
