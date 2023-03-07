from django.test import TestCase
from django.test import Client
from django.urls import reverse
from users.models import User
from clothes.models import Product,Clothes,Categories
from markets.models import Market


class OrderTest(TestCase):
    def test_order_without_user(self):
        c=Client()
        product_id = Product.objects.filter(name='맨투맨1').first().id
        url = reverse('orders:order',args=(product_id,))
        response = c.get(url)
        print(response)
        self.assertEqual(response.url,1)
    def test_order_with_user(self):
        c=Client()
        product_id = Product.objects.filter(name='맨투맨1').first().id
        url = reverse('orders:order',args=(product_id,))
        c.login(username="test2@test.com",password="test2")
        response = c.get(url)
        print(response)
        self.assertEqual(response.status_code,302)

    