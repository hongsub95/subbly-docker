from django.urls import path
from . import views

app_name = "orders_api"

urlpatterns = [
    path('',views.AdminOrderListCreateAPIView.as_view()),
    
]
