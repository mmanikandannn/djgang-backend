from rest_framework import serializers

from cart.models import Cart
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "size", "price", "qty", "line_total"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "full_name", "email", "phone", "address", "city", "pincode",
            "subtotal", "shipping_fee", "total", "payment_method", "is_paid", "status",
            "items", "created_at",
        ]
        read_only_fields = ["order_number", "subtotal", "total", "is_paid", "status", "created_at"]


class OrderCreateSerializer(serializers.Serializer):
    """Creates an order from the user's current cart, then clears it."""

    full_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField()
    pincode = serializers.CharField()
    payment_method = serializers.ChoiceField(choices=Order.PaymentMethod.choices, default=Order.PaymentMethod.RAZORPAY)

    def create(self, validated_data):
        user = self.context["request"].user
        cart = Cart.objects.filter(user=user).first()
        if not cart or not cart.items.exists():
            raise serializers.ValidationError("Your cart is empty.")

        subtotal = cart.subtotal
        shipping_fee = 99
        order = Order.objects.create(
            user=user,
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            total=subtotal + shipping_fee,
            **validated_data,
        )
        for item in cart.items.select_related("product"):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                size=item.size,
                price=item.product.price,
                qty=item.qty,
            )
        cart.items.all().delete()
        return order
