from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('<int:pk>/',views.OrderView,name="order"),
    path('<int:pk>/complete/',views.OrderCompleteView,name="order-complete")
]
