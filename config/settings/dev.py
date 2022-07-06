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
    "core.apps.CoreConfig",
    "clothes.apps.ClothesConfig",
    "markets.apps.MarketsConfig",
    "options.apps.OptionsConfig",
    "lists.apps.ListsConfig",
]

THIRD_APPS = [
    "bootstrap5",
    "rest_framework",
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_APPS