from rest_framework import serializers
from clothes import models as clothes_models
from markets import models as markets_models
from markets import serializers as markets_serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = clothes_models.Categories
        fields = ("name",)



class ClothesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    market = markets_serializers.MarketSerialzer()
    
    class Meta:
        model = clothes_models.Clothes
        exclude = ()

class ClothesCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    market = markets_serializers.MarketSerialzer()
    

    class Meta:
        model = clothes_models.Clothes
        exclude = ()
        read_only_fields = ("host", "pk", "created", "updated", "market")

    def create(self, validated_data):
        request = self.context.get("request")
        categories_data = validated_data.pop("category")
        markets_data = validated_data.pop("market")
        sizes_data = validated_data.pop("size")
        colors_data = validated_data.pop("colors")
        clothes = clothes_models.Clothes.objects.create(
            **validated_data, host=request.user
        )
        for category_data in categories_data:
            clothes_models.Categories.objects.create(clothes=clothes, **category_data)
        for market_data in markets_data:
            markets_models.Market.objects.create(clothes=clothes, **market_data)
        
        return clothes

class ClothesPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = clothes_models.Clothes
        exclude = ()
        
    