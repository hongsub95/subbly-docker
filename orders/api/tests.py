from rest_framework.test import APITestCase,APIRequestFactory,force_authenticate,APIClient
from django.test.client import encode_multipart,RequestFactory
from django.urls import reverse

from orders.models import Order
from orders.orderid import MakeOrderId
from users.models import User
from clothes.models import Product,Clothes,Categories
from markets.models import Market
from orders.api.views import AdminOrderListCreateAPIView,AdminOrderRetrieveUpdateDestroyAPIView
from clothes.api.serializers import ClothesSerializer,ProductSerializer,CategorySerializer
from markets.serializers import MarketSerialzer
from users.api.serializers import UserSerializer

from config.settings.common import SECRET_KEY,ALGORITHM

import json
import jwt

class OrderAPITest(APITestCase):
    order_id = MakeOrderId()
    orderstate = Order.OrderState.purchase
    address = "인천광역시 부평구"
    paycate = Order.PayChoice.cash
    product = Product.objects.filter(id=140).values()
    user = User.objects.filter(id=2).values()
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user1 = User.objects.create(
                username="test001@test.com",
                password="user001",
                name="user001",
                login_method=User.LoginChoices.EMAIL,
                gender=User.GenderChoices.MALE
            )
            
        cls.user2 = User.objects.create(
                username="test002@test.com",
                password="user002",
                name="user002",
                login_method=User.LoginChoices.EMAIL,
                gender=User.GenderChoices.MALE
            )
        cls.category = Categories.objects.create(
                name="상의"
            )
        cls.market = Market.objects.create(
                name="형아네옷가게",
                phone_number="000000000",
                market_url="market1@test.com",
                description="형아네 옷가게 입니다",
                master=cls.user2
            )
        cls.clothes = Clothes.objects.create(
                name="맨투맨",
                description="아주 예쁜옷",
                price=30000,
                category=cls.category,
                market=cls.market
            )
        cls.product = Product.objects.create(
                clothes=cls.clothes,
                name="맨투맨",
                price=30000,
                description="아주 예쁜옷",
                stock=200,
                colors="베이직"
                ,size="S",
                category=cls.category,
                market=cls.market,
                is_sold_out=False
                )
        cls.token = jwt.encode({'username':cls.user1.username},SECRET_KEY,algorithm=ALGORITHM)
        cls.product_serializer = ProductSerializer(cls.product)
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
    
    def test_order_post(self):
        factory = APIRequestFactory()
        admin = User.objects.get(pk=1)
        product = {
            "id":self.product.pk,
            "clothes_id":self.product.clothes.pk,
            "name": self.product.name,
            "description": self.product.description,
            "price": 30000,
            "stock":self.product.stock,
            "colors":"네이비",
            "category": Categories.objects.filter(name="상의").first().id,
            "market": Market.objects.filter(name="형아네옷가게").first().id,
            "size":"33",
            "is_sold_out":False,
            "created":self.product.created.strftime('%Y-%m-%d'),
            "deleted_at":self.product.deleted_at,
            "updated":self.product.updated.strftime('%Y-%m-%d')
        }
        user = {
            "id":self.user1.pk,
            "is_superuser":self.user1.is_superuser,
            "username":self.user1.username,
            "is_staff":self.user1.is_staff,
            "name":self.user1.name,
            "login_method":"EMAIL",
            "superhost":self.user1.superhost,
        }
        data = {
            "order_id":self.order_id,
            "product":product,
            "buyer":user,
            "orderstate":self.orderstate,
            "address":self.address,
            "paycate":self.paycate,
        }
        request =factory.post(reverse("orders_api:order_api_list_create"),json.dumps(data),content_type='application/json')
        force_authenticate(request,user=admin)
        view = AdminOrderListCreateAPIView.as_view()
        response = view(request)
        print(response)
        self.assertEqual(response.status_code,201)
    '''
    def test_order_patch(self):
        factory = APIRequestFactory()
        order = Order.objects.create(
            order_id = self.order_id,
            buyer = self.buyer,
            product = self.product,
            orderstate = self.orderstate,
            address = self.address,
            paycate = self.paycate,)
        admin = User.objects.get(pk=1)
        product2=Product.objects.get(pk=3)
        data = {
            "product":product2,
        }
        request =factory.patch("/api/v1/orders/admin/1/",data,content_type="application/json")
        force_authenticate(request,user=admin)
        view = AdminOrderRetrieveUpdateDestroyAPIView.as_view()
        response = AdminOrderRetrieveUpdateDestroyAPIView.as_view()(request)
        print(response)
    '''
        