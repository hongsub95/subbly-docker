from rest_framework import serializers
from . import models


class SizeSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.Size
        fields = ("size",)


class ColorSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.Color
        fields = ("color",)
