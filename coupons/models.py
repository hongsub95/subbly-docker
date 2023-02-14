from django.db import models
from django.contrib import messages
from config.models import SoftDeleteModel

class Coupon(SoftDeleteModel):
    class CouponChoice(models.TextChoices):
        fixed_rate = "Fix","정률쿠폰"
        flat_rate = "Flat","정액쿠폰"
    coupon_id = models.CharField(max_length=16,unique=True,verbose_name="쿠폰아이디")
    name = models.CharField(max_length=30,unique=True,verbose_name="이름")
    description = models.TextField(verbose_name="내용")
    min_price = models.BigIntegerField(null=True,blank=True,verbose_name="최소금액")
    discount = models.IntegerField(verbose_name="할인") # 쿠폰종류가 정률쿠폰이면 50미만(%로 계산), 정액쿠폰이면 최소금액보다 작아야함(원으로 계산)
    is_issued = models.BooleanField(default=False,verbose_name="발급여부")
    is_used = models.BooleanField(default=False,verbose_name="사용여부")
    coupon_cate = models.CharField(max_length=20,choices=CouponChoice.choices,verbose_name="쿠폰종류")
    owner = models.ForeignKey("users.User",null=True,blank=True,related_name="coupon",on_delete=models.CASCADE,verbose_name="소유자")
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural ="쿠폰"
    