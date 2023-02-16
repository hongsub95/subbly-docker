from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe


class clothes_photo(admin.TabularInline):
    model = models.photo
    


@admin.register(models.photo)
class PhotoAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "photo Info",
            {
                "fields": (
                    "name",
                    "file",
                    "product"
                ),
            },
        ),
    )
    list_display = (
        "product",
        "get_thumbnail",
        
    )

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "썸네일"


@admin.register(models.Categories)
class CateAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Clothes)
class ClothesAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Clothes Info",
            {
                "fields": (
                    "name",
                    "description",
                    "category",
                    "price",
                    "market",
                ),
            },
        ),
    )
    list_display = (
        "name",
        "price",
        "category",
    )
    search_fields = ("name", )
    raw_id_fields = ( "market",)
    inlines = [
        clothes_photo,
    ]

