from django.contrib import admin

from .models import Track


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "duration", "release_date", "order", "is_published")
    list_filter = ("genre", "is_published")
    search_fields = ("title",)
    list_editable = ("order", "is_published")
