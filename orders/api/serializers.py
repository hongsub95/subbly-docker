from rest_framework import serializers

from orders.models import Order
from users.api.serializers import UserSerializer
from coupons.api.serializers import CouponSerializer
from clothes.api.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    buyer = UserSerializer()
    coupon = CouponSerializer()
    product = ProductSerializer()
    class Meta:
        model = Order
        fields = ["order_id","buyer","product","orderstate","address","paycate","coupon","deleted_at","created","updated"]

class OrderCreateSerailizer(serializers.ModelSerializer):
    buyer = UserSerializer()
    coupon = CouponSerializer()
    product = ProductSerializer()
    class Meta:
        model = Order
        fields = ["order_id","buyer","product","orderstate","address","paycate","coupon","deleted_at","created","updated"]
        
        
    