from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_MALE = "Male"
    GENDER_FEMALE = "Female"
    GENDER_OTHER = "Other"
    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    ]
    LOGIN_EMAIL = "email"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_KAKAO, "Kakao"),
    )
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )
    avatar = models.ImageField(blank=True, upload_to="avatar", verbose_name="프로필 사진")
    gender = models.CharField(
        max_length=10, null=True, blank=True, choices=GENDER_CHOICES, verbose_name="성별"
    )
    height = models.IntegerField(blank=True, null=True, verbose_name="키")
    weight = models.IntegerField(blank=True, null=True, verbose_name="몸무게")
    birthday = models.DateField(null=True, blank=True, verbose_name="생년월일")
    superhost = models.BooleanField(default=False, blank=True)
    bio = models.TextField(default="", blank=True, verbose_name="자기소개")
