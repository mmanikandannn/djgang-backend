from django.conf import settings
from django.db import models

from catalog.models import Product


class Cart(models.Model):
    """One cart per authenticated user. Anonymous carts are handled
    client-side (localStorage) until login, then merged via the /merge/ endpoint."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart #{self.pk} ({self.user.email})"

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.items.all())

    @property
    def count(self):
        return sum(item.qty for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=20, blank=True)
    qty = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "product", "size")

    def __str__(self):
        return f"{self.qty} x {self.product.name} ({self.size})"

    @property
    def line_total(self):
        return self.product.price * self.qty
