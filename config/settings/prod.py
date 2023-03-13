from .common import *

DEBUG = False

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "3.35.4.104"
]

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
    "coupons.apps.CouponsConfig",
    "orders.apps.OrdersConfig",
]

THIRD_APPS = [
    "bootstrap5",
    "rest_framework",
    "storages",
    "rest_framework_swagger",
    'rest_framework_simplejwt',
    'drf_yasg',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_APPS

'''
# AWS S3 쓸때 재활용 ㄱㄱ
AWS_S3_SECURE_URLS = False       # use http instead of https
AWS_QUERYSTRING_AUTH = False     # don't add complex authentication-related query parameters for requests
DEFAULT_FILE_STORAGE = "config.settings.custom_storages.upload_storage"
STATICFILES_STORAGE = "config.settings.custom_storages.static_storage"
AWS_S3_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 's3-subbly'
AWS_DEFAULT_ACL= "public-read"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
'''
