from rest_framework import serializers
from django.db import transaction

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
        fields = ["pk","order_id","buyer","product","orderstate","address","paycate","coupon","deleted_at","created","updated"]

class OrderPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["pk","order_id","buyer","product","orderstate","address","paycate","coupon","deleted_at","created","updated"]
class OrderCreateSerailizer(serializers.ModelSerializer):
    buyer = UserSerializer()
    coupon = CouponSerializer()
    product = ProductSerializer()
    
    class Meta:
        model = Order
        fields = ["pk","order_id","buyer","product","orderstate","address","paycate","coupon","deleted_at","created","updated"]
        
    @transaction.atomic
    def create(self, validated_data):
        order_id = validated_data.pop('order_id')
        buyer = validated_data.pop('buyer')
        product = validated_data.pop('product')
        orderstate = validated_data.pop('orderstate')
        address = validated_data.pop('address')
        paycate = validated_data.pop('paycate')
        coupon = validated_data.pop('coupon')

        return Order.objects.create(order_id = order_id,buyer=buyer,product=product,orderstate=orderstate,address=address,paycate=paycate,coupon=coupon,**validated_data)
        
        
    