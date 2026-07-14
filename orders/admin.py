from django.contrib import admin
from django.utils.html import format_html

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "size", "price", "qty")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "full_name", "email", "total", "payment_method", "status_badge", "is_paid", "created_at")
    list_filter = ("status", "payment_method", "is_paid")
    search_fields = ("order_number", "full_name", "email", "phone")
    readonly_fields = ("order_number", "subtotal", "total", "created_at", "updated_at")
    inlines = [OrderItemInline]
    list_editable = ()

    fieldsets = (
        ("Order", {"fields": ("order_number", "user", "status")}),
        ("Customer", {"fields": ("full_name", "email", "phone", "address", "city", "pincode")}),
        ("Payment", {"fields": ("payment_method", "razorpay_order_id", "razorpay_payment_id", "is_paid")}),
        ("Totals", {"fields": ("subtotal", "shipping_fee", "total")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    status_colors = {
        "PENDING": "#f5a623",
        "CONFIRMED": "#00c2ff",
        "SHIPPED": "#9b3bff",
        "DELIVERED": "#2ecc71",
        "CANCELLED": "#ff4d4d",
    }

    @admin.display(description="Status")
    def status_badge(self, obj):
        color = self.status_colors.get(obj.status, "#999")
        return format_html('<span style="color:{};font-weight:600;">{}</span>', color, obj.get_status_display())
