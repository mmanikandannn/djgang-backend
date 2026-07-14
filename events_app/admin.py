from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "city", "venue", "status", "is_published")
    list_filter = ("status", "is_published")
    search_fields = ("title", "city", "venue")
    list_editable = ("status", "is_published")
    date_hierarchy = "date"
