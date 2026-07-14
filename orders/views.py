from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    GET  /api/orders/            -> current user's orders (or all, for staff)
    POST /api/orders/            -> place an order from the current cart
    GET  /api/orders/<id>/       -> order detail
    PATCH /api/orders/<id>/      -> staff-only: update status
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().prefetch_related("items")
        return Order.objects.filter(user=user).prefetch_related("items")

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # --- Razorpay placeholder -------------------------------------------------
        # if order.payment_method == Order.PaymentMethod.RAZORPAY:
        #     import razorpay
        #     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        #     rp_order = client.order.create({
        #         "amount": int(order.total * 100),
        #         "currency": "INR",
        #         "receipt": order.order_number,
        #     })
        #     order.razorpay_order_id = rp_order["id"]
        #     order.save()
        # ----------------------------------------------------------------------------

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "Only staff can update order status."}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def mark_paid(self, request, pk=None):
        order = self.get_object()
        order.is_paid = True
        order.status = Order.Status.CONFIRMED
        order.save()
        return Response(OrderSerializer(order).data)
