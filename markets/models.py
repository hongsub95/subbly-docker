from django.db import models
from core import models as core_models


class Market(core_models.TimeStampedModel):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13)
    market_url = models.URLField(max_length=200, verbose_name="사이트")

    def __str__(self):
        self.name

    class Meta:
        verbose_name_plural = "마켓"
