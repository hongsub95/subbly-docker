from rest_framework import serializers

from django.db import transaction

from clothes.models import Clothes,Product,Categories
from markets import models as markets_models
from markets import serializers as markets_serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        exclude = ()
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ()

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

class ClothesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    market = markets_serializers.MarketSerialzer()
    product = ProductSerializer(many=True)
    
    class Meta:
        model = Clothes
        fields = ["name","description","price","category","market","product"]

class ClothesCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    market = markets_serializers.MarketSerialzer()
    

    class Meta:
        model = Clothes
        exclude = ()
        read_only_fields = ("host", "pk", "created", "updated", "market")
    
    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get("request")
        clothes = Clothes.objects.create(
            **validated_data, host=request.user
        )
        return clothes

class ClothesPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        exclude = ()



        
    