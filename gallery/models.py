from django.db import models


class GalleryImage(models.Model):
    class Category(models.TextChoices):
        LIVE = "LIVE", "Live Show"
        STUDIO = "STUDIO", "Studio"
        BACKSTAGE = "BACKSTAGE", "Backstage"
        FESTIVAL = "FESTIVAL", "Festival"

    title = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.LIVE)
    image = models.ImageField(upload_to="gallery/")
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-uploaded_at"]

    def __str__(self):
        return self.title or f"Gallery image #{self.pk}"
