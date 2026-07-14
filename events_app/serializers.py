from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id", "title", "genre", "venue", "city", "date", "time",
            "status", "ticket_url", "image", "is_published",
        ]
