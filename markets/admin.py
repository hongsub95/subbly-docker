from django.contrib import admin
from . import models


@admin.register(models.Market)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "market_url",
    )
