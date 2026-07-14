from rest_framework import serializers

from .models import BookingEnquiry


class BookingEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingEnquiry
        fields = [
            "id", "name", "email", "phone", "event_type", "event_date",
            "city", "budget", "details", "status", "created_at",
        ]
        read_only_fields = ["status", "created_at"]
