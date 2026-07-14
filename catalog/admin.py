from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "category", "price", "stock", "stock_status", "is_digital", "is_active", "tag")
    list_filter = ("category", "is_digital", "is_active", "tag")
    search_fields = ("name", "description")
    list_editable = ("price", "stock", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {"fields": ("name", "slug", "category", "description")}),
        ("Pricing & Stock", {"fields": ("price", "compare_at_price", "stock", "sizes")}),
        ("Media", {"fields": ("image",)}),
        ("Digital Product", {"fields": ("is_digital", "digital_file")}),
        ("Display", {"fields": ("tag", "rating", "is_active")}),
    )

    @admin.display(description="")
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.image.url)
        return "—"

    @admin.display(description="Stock Status")
    def stock_status(self, obj):
        if obj.is_digital:
            return format_html('<span style="color:#00c2ff;">Digital</span>')
        if obj.stock == 0:
            return format_html('<span style="color:#ff4d4d;">Out of stock</span>')
        if obj.stock < 5:
            return format_html('<span style="color:#f5a623;">Low stock</span>')
        return format_html('<span style="color:#2ecc71;">In stock</span>')
