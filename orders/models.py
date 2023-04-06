from django.db import models
from config.models import SoftDeleteModel

class Order(SoftDeleteModel):
    class OrderState(models.TextChoices):
        completed = "complete","배송완료"
        shipping = "shipping","배송중"
        purchase = "purchase","구매완료"
        exchange = "exchange","교환"
    class PayChoice(models.TextChoices):
        card = "card","카드"
        cash = "cash","계좌이체"
    order_id = models.CharField(max_length=15,null=True)
    buyer = models.ForeignKey("users.User",related_name="order",on_delete=models.CASCADE)
    product = models.ForeignKey("clothes.Product",related_name="order",on_delete=models.CASCADE)
    orderstate = models.CharField(max_length=20,choices=OrderState.choices,default=OrderState.purchase)
    address = models.CharField(max_length = 100, null=True,verbose_name="주소")
    paycate = models.CharField(max_length=10,choices=PayChoice.choices,default=PayChoice.cash)
    coupon = models.ForeignKey("coupons.Coupon",blank=True,null=True,related_name="order",on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created']
