from django.db import models


class BookingEnquiry(models.Model):
    class EventType(models.TextChoices):
        CLUB = "CLUB", "Club Night"
        FESTIVAL = "FESTIVAL", "Festival"
        PRIVATE = "PRIVATE", "Private Party"
        CORPORATE = "CORPORATE", "Corporate Event"
        WEDDING = "WEDDING", "Wedding"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        NEW = "NEW", "New"
        CONTACTED = "CONTACTED", "Contacted"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CLOSED = "CLOSED", "Closed"

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_type = models.CharField(max_length=20, choices=EventType.choices, default=EventType.CLUB)
    event_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=120, blank=True)
    budget = models.CharField(max_length=50, blank=True)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Booking Enquiry"
        verbose_name_plural = "Booking Enquiries"

    def __str__(self):
        return f"{self.name} - {self.event_type} ({self.event_date})"
