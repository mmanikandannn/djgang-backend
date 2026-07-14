from django.db import models


class Track(models.Model):
    class Genre(models.TextChoices):
        PSYTRANCE = "PSYTRANCE", "Psytrance"
        HITECH = "HITECH", "Hi-Tech"
        TECHNO = "TECHNO", "Techno"
        EDM = "EDM", "EDM"
        MELODIC_TECHNO = "MELODIC_TECHNO", "Melodic Techno"

    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=30, choices=Genre.choices, default=Genre.PSYTRANCE)
    youtube_url = models.URLField(blank=True)
    soundcloud_url = models.URLField(blank=True)
    audio_file = models.FileField(upload_to="tracks/", blank=True, null=True, help_text="Optional direct audio upload")
    cover_image = models.ImageField(upload_to="tracks/covers/", blank=True, null=True)
    duration = models.CharField(max_length=10, blank=True, help_text="e.g. 58:20")
    release_date = models.DateField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-release_date"]

    def __str__(self):
        return self.title
