from django.db import models
from core import models as core_models
from users import models as User_models


class Market(core_models.TimeStampedModel):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13)
    market_url = models.URLField(max_length=200, verbose_name="사이트")
    description = models.TextField(verbose_name="설명")
    master = models.OneToOneField(User_models.User,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "마켓"
