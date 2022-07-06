from django.db import models
from core import models as core_models


class Color(core_models.TimeStampedModel):

    color = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "색상"
        verbose_name = "색상"

    def __str__(self):
        return self.color


class Size(core_models.TimeStampedModel):

    size = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "사이즈"

    def __str__(self):
        return self.size
