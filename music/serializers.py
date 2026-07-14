from rest_framework import serializers

from .models import Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = [
            "id", "title", "genre", "youtube_url", "soundcloud_url", "audio_file",
            "cover_image", "duration", "release_date", "is_published", "order",
        ]
