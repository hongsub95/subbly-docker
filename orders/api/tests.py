from rest_framework.test import APITestCase,APIRequestFactory,force_authenticate
from django.urls import reverse

from orders.models import Order
from orders.orderid import MakeOrderIdNum
from users.models import User
from clothes.models import Product
from orders.api.views import AdminOrderListCreateAPIView

class OrderAPITest(APITestCase):
    order_id = MakeOrderIdNum()
    buyer = User.objects.get(pk=2)
    product = Product.objects.get(pk=2)
    orderstate = Order.OrderState.purchase
    address = "인천광역시 부평구 "
    paycate = Order.PayChoice.cash
    def test_order_get_with_admin(self):
        factory = APIRequestFactory(enforce_csrf_checks=True)
        admin = User.objects.get(pk=1)
        request =factory.get(reverse("orders_api:order_api_list_create"))
        view = AdminOrderListCreateAPIView.as_view() 
        force_authenticate(request,user=admin)
        response = view(request)
        self.assertEqual(response.status_code,200)
    
    def test_order_get_without_admin(self):
        factory = APIRequestFactory(enforce_csrf_checks=True)
        request =factory.get(reverse("orders_api:order_api_list_create"))
        view = AdminOrderListCreateAPIView.as_view() 
        response = view(request)
        self.assertEqual(response.status_code,401)  # 401은 미승인(unauthorized), 정확히는 비인증(unauthenticated)을 의미
    
    def test_order_create(self):
        factory = APIRequestFactory(enforce_csrf_checks=True)
        admin = User.objects.get(pk=1)
        data = {
            "order_id":self.order_id,
            "buyer":self.buyer,
            "product":self.product,
            "orderstate":self.orderstate,
            "address":self.address,
            "paycate":self.paycate,
        }
        request =factory.post(reverse("orders_api:order_api_list_create"),data,format="json")
        view = AdminOrderListCreateAPIView.as_view() 
        force_authenticate(request,user=admin)
        response = view(request)
        self.assertEqual(response.status_code,201)