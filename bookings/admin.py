from django.contrib import admin

from .models import BookingEnquiry


@admin.register(BookingEnquiry)
class BookingEnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "event_type", "event_date", "city", "phone", "status", "created_at")
    list_filter = ("status", "event_type")
    search_fields = ("name", "email", "phone", "city")
    list_editable = ("status",)
    readonly_fields = ("created_at",)
