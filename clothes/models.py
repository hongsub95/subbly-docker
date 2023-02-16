from multiprocessing.sharedctypes import Value
from tabnanny import verbose
from django.db import models
from django.shortcuts import reverse
from config.models import SoftDeleteModel


class photo(SoftDeleteModel):
    name = models.CharField(max_length=30)
    file = models.ImageField(upload_to="product")
    product = models.ForeignKey(
        "Clothes", related_name="photo", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "상품 사진"


class Categories(SoftDeleteModel):
    name = models.CharField(max_length=20, verbose_name="이름")

    class Meta:
        verbose_name_plural = "카테고리"

    def __str__(self):
        return self.name

#전시용
class Clothes(SoftDeleteModel):
    name = models.CharField(max_length=100, verbose_name="상품명")
    description = models.TextField(verbose_name="설명")
    price = models.IntegerField(verbose_name="가격")
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

    def thumbnail(self):
        img_name = self.name
        try:
            photo = self.photo.get(name=f'{img_name}')
            return photo.file.url
        except IndexError:
            return None
        
    class Meta:
        verbose_name_plural = "상품"
        ordering = ['-id']

    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        return reverse("clothes:clothes_detail", kwargs={"pk": self.pk})

#내부용
class Product(SoftDeleteModel):
    clothes = models.ForeignKey("clothes",on_delete=models.DO_NOTHING,related_name='product')
    name = models.CharField(max_length=100, verbose_name="상품명")
    price = models.IntegerField(verbose_name="가격")
    description = models.TextField(verbose_name="설명")
    stock = models.IntegerField(verbose_name="재고")
    colors = models.CharField(
        max_length=20,verbose_name="색상"
    )
    size = models.CharField(
        max_length=20,verbose_name="사이즈"
    )
    category = models.ForeignKey(
        "Categories",
        related_name="product",
        on_delete=models.DO_NOTHING,
        verbose_name="카테고리",
        null=True,
        blank=True,
    )
    market = models.ForeignKey(
        "markets.Market",
        related_name="product",
        on_delete=models.CASCADE,
        verbose_name="사이트",
        null=True,
        blank=True,
    )
    is_sold_out = models.BooleanField(verbose_name="품절여부",default=False)
    
    
    class Meta:
        ordering = ['-id']