# 개발용
from .common import *


DEBUG = True

ALLOWED_HOSTS = [
    
]


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    "users.apps.UsersConfig",
    "clothes.apps.ClothesConfig",
    "markets.apps.MarketsConfig",
    "lists.apps.ListsConfig",
    "seed.apps.SeedConfig",
    "coupons.apps.CouponsConfig",
    "orders.apps.OrdersConfig",
]

THIRD_APPS = [
    "bootstrap5",
    "rest_framework",
    "rest_framework_swagger",
    "rest_framework_simplejwt",
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_APPS