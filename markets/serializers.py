from rest_framework import serializers
from markets import models


class MarketSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.Market
        fields = ("name",)
