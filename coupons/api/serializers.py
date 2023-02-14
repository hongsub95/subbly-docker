from rest_framework import serializers
from django.db import transaction
from coupons.models import Coupon
from coupons.services import MakeCouponNum

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ["pk","coupon_id","name","description","min_price","discount","is_issued","is_used","coupon_cate","owner","created_at","deleted_at"]

class CouponCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ["pk","coupon_id","name","description","min_price","discount","is_issued","is_used","coupon_cate","owner","created_at","deleted_at"]
    @transaction.atomic
    def create(self, validated_data):
        coupon_id = validated_data.pop('coupon_id')
        name = validated_data.pop('name')
        min_price = validated_data.pop('min_price')
        coupon_cate = validated_data.pop('coupon_cate')
        discount = validated_data.pop('discount')
        if coupon_cate == "Fix":
            if discount > 50:
                raise serializers.ValidationError("할인률을 50을 초과 할 수 없습니다.")
        else:
            if discount >= min_price:
                raise serializers.ValidationError("할인금액이 최소금액보다 클 수 없습니다.")
        coupon_id = MakeCouponNum()
        return Coupon.objects.create(coupon_id = coupon_id,name=name,min_price=min_price,coupon_cate=coupon_cate,discount=discount,**validated_data)
        

class CouponPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ["pk","coupon_id","name","description","min_price","discount","is_issued","is_used","coupon_cate","owner","created_at","delete_date","deleted_at"] 

class CouponDeleteSerializer(serializers.ModelSerializer):
    pass
    