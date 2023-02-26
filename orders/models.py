from django.db import models

class Order(models.Model):
    class OrderState(models.TextChoices):
        completed = "complete","배송완료"
        shipping = "shipping","배송중"
        purchase = "purchase","구매완료"
        exchange = "exchange","교환"
    buyer = models.ForeignKey("users.User",related_name="order",on_delete=models.CASCADE)
    product = models.ForeignKey("clothes.Product",related_name="order",on_delete=models.CASCADE)
    orderstate = models.CharField(max_length=20,choices=OrderState.choices,default=OrderState.purchase)
    created = models.DateTimeField('생성일',auto_now_add=True)
    updated = models.DateTimeField('수정일',auto_now=True)
