from django.db import models


class Event(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Tickets Available"
        SELLING_FAST = "SELLING_FAST", "Selling Fast"
        SOLD_OUT = "SOLD_OUT", "Sold Out"

    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=120, blank=True)
    venue = models.CharField(max_length=150)
    city = models.CharField(max_length=120)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    ticket_url = models.URLField(blank=True, help_text="External ticketing link, or leave blank to link to Shop event passes")
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.title} - {self.date}"
