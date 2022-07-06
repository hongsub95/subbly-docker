from rest_framework import serializers
from clothes import models as clothes_models
from options import models as options_models
from markets import models as markets_models
from markets import serializers as markets_serializers
from options import serializers as options_serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = clothes_models.Categories
        fields = ("name",)


class ClothesSerializer(serializers.ModelSerializer):
    colors = options_serializers.ColorSerialzer(many=True)
    category = CategorySerializer()
    market = markets_serializers.MarketSerialzer()
    size = options_serializers.SizeSerialzer(many=True)

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
        for size_data in sizes_data:
            options_models.Size.objects.create(clothes=clothes, **size_data)
        for color_data in colors_data:
            options_models.Color.objects.create(clothes=clothes, **color_data)

        return clothes
