from django.contrib import admin
from django.utils.html import format_html

from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "category", "order", "is_published")
    list_filter = ("category", "is_published")
    list_editable = ("order", "is_published")

    @admin.display(description="Preview")
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;border-radius:6px;" />', obj.image.url)
        return "—"
