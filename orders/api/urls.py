from django.urls import path
from . import views

app_name = "orders_api"

urlpatterns = [
    path('admin/',views.AdminOrderListCreateAPIView.as_view(),name="order_api_list_create"),
    path('admin/<int:pk>/',views.AdminOrderRetrieveUpdateDestroyAPIView.as_view(),name="order_api_retrieve_update_delete")
    
]
