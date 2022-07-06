from django.db import models
from core import models as core_models


class List(core_models.TimeStampedModel):
    list_id = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.list_id


class ListItem(core_models.TimeStampedModel):
    clothes = models.ForeignKey(
        "clothes.Clothes",
        verbose_name="상품",
        related_name="list",
        on_delete=models.CASCADE,
    )
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "장바구니"

    def __str__(self):
        return f"{self.user}님의 장바구니"
