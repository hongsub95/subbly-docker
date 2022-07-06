from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe


class clothes_photo(admin.TabularInline):
    model = models.photo


@admin.register(models.photo)
class PhotoAdmin(admin.ModelAdmin):
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
                    "stock",
                    "colors",
                    "price",
                    "size",
                    "market",
                    "host",
                ),
            },
        ),
    )
    filter_horizontal = ("size", "colors")
    list_display = (
        "name",
        "color",
        "price",
        "category",
        "host",
    )
    search_fields = ("name", "colors")
    raw_id_fields = ("host", "market")
    inlines = [
        clothes_photo,
    ]

    def color(self, obj):
        c = obj.colors.all()
        color_list = []
        for co in c:
            color_list.append(co)
        return color_list if len(color_list) < 5 else color_list[:5]

    color.short_description = "색상"
