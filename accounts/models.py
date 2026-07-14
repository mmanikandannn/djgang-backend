from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user so we can extend it later (loyalty points, phone, etc.)
    without a painful migration down the line."""

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    is_customer = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
