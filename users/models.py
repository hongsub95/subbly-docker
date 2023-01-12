from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성" 
    class LoginChoices(models.TextChoices):
        KAKAO = "KAKAO","카카오"
        EMAIL = "EMAIL","이메일"
    first_name = None
    last_name = None
    name = models.CharField(max_length=20,verbose_name="이름")
    login_method = models.CharField(
        max_length=50, choices=LoginChoices.choices, default=LoginChoices.EMAIL
    )
    avatar = models.ImageField(blank=True, upload_to="avatar", verbose_name="프로필 사진")
    gender = models.CharField(
        max_length=10, null=True, blank=True, choices=GenderChoices.choices, verbose_name="성별"
    )
    height = models.IntegerField(blank=True, null=True, verbose_name="키")
    weight = models.IntegerField(blank=True, null=True, verbose_name="몸무게")
    birthday = models.DateField(null=True, blank=True, verbose_name="생년월일")
    superhost = models.BooleanField(default=False, blank=True)
    bio = models.TextField(default="", blank=True, verbose_name="자기소개")
