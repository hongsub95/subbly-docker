from multiprocessing.sharedctypes import Value
from tabnanny import verbose
from django.db import models
from django.shortcuts import reverse
from core import models as core_models


class photo(core_models.TimeStampedModel):
    name = models.CharField(max_length=30)
    file = models.ImageField(upload_to="product")
    product = models.ForeignKey(
        "Clothes", related_name="photo", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "상품 사진"


class Categories(core_models.TimeStampedModel):
    name = models.CharField(max_length=20, verbose_name="이름")

    class Meta:
        verbose_name_plural = "카테고리"

    def __str__(self):
        return self.name


class Clothes(core_models.TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name="상품명")
    description = models.TextField(verbose_name="설명")
    price = models.IntegerField(verbose_name="가격")
    stock = models.IntegerField(verbose_name="재고")
    colors = models.ManyToManyField(
        "options.Color", related_name="clothes", blank=True, verbose_name="색상"
    )
    size = models.ManyToManyField(
        "options.Size", related_name="clothes", blank=True, verbose_name="사이즈"
    )
    category = models.ForeignKey(
        "Categories",
        related_name="clothes",
        on_delete=models.DO_NOTHING,
        verbose_name="카테고리",
        null=True,
        blank=True,
    )
    market = models.ForeignKey(
        "markets.Market",
        related_name="clothes",
        on_delete=models.CASCADE,
        verbose_name="사이트",
        null=True,
        blank=True,
    )
    host = models.ForeignKey(
        "users.User",
        related_name="clothes",
        on_delete=models.CASCADE,
        verbose_name="판매자",
    )

    def thumbnail(self):
        try:
            photo = self.photo.all()[0]
            return photo.file.url
        except ValueError:
            return None

    class Meta:
        verbose_name_plural = "상품"

    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        return reverse("clothes:clothes_detail", kwargs={"pk": self.pk})

  