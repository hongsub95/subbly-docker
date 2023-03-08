from django.test import TestCase
from django.test import Client
from django.urls import reverse

from orders.orderid import MakeOrderIdNum
from users.models import User
from clothes.models import Product,Clothes,Categories
from markets.models import Market

import json

class OrderTest(TestCase):
    '''
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="test10@test.com", password="test2", name="user2", gender=User.GenderChoices.MALE)
        Market.objects.create(name="형아네옷가게", market_url="https://www.abc1.co.kr", master_id=User.objects.filter(username="test10@test.com").first().id, description='형아네와 함께 멋진 스타일을 완성해보세요. #간편한 룩 #2030 #판교')
        Categories.objects.create(name="상의")
        Clothes.objects.create(name='맨투맨1',description='인기많은 맨투맨',price=30000,category_id=Categories.objects.filter(name='상의').first().id,market_id=Market.objects.filter(name='형아네옷가게').first().id)
        Product.objects.create(clothes_id=Clothes.objects.filter(name='맨투맨1').first().id,
                name='맨투맨',
                description='인기많은 맨투맨',
                price=30000,
                stock=100,
                category_id=Categories.objects.filter(name='상의').first().id,
                market_id=Market.objects.filter(name='형아네옷가게').first().id,
                size='M',
                colors ="red",
                is_sold_out=False)
    '''
    def test_order_without_user(self): # 로그인 인증 안된상태에서 구매하면 로그인 화면 창으로 이동
        c=Client()
        product_id = Product.objects.filter(name='맨투맨1').first().id
        url = reverse('orders:order',args=(product_id,))
        response = c.get(url)
        self.assertEqual(response.url,f'/users/login/?next=/orders/{product_id}/')
        
    def test_order_with_user(self):
        c=Client()
        product_id = Product.objects.filter(name='맨투맨1').first().id
        user = User.objects.get(pk=2)
        url = reverse('orders:order',args=(product_id,))
        c.force_login(user=user)
        response = c.get(url)
        self.assertEqual(response.url,f'/clothes/{product_id}/')
        self.assertEqual(response.status_code,302)


        
        
    