from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem
from .serializers import CartSerializer


class CartView(APIView):
    """
    GET    /api/cart/                 -> current user's cart
    POST   /api/cart/items/           -> add item {product_id, size, qty}
    PATCH  /api/cart/items/<id>/      -> update qty {qty}
    DELETE /api/cart/items/<id>/      -> remove item
    DELETE /api/cart/                 -> clear cart
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request):
        cart = self.get_cart(request.user)
        return Response(CartSerializer(cart).data)

    def delete(self, request):
        cart = self.get_cart(request.user)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data)


class CartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get("product_id")
        size = request.data.get("size", "")
        qty = int(request.data.get("qty", 1))

        item, created = CartItem.objects.get_or_create(
            cart=cart, product_id=product_id, size=size, defaults={"qty": qty}
        )
        if not created:
            item.qty += qty
            item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    def patch(self, request, item_id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item = cart.items.filter(id=item_id).first()
        if not item:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        qty = int(request.data.get("qty", item.qty))
        item.qty = max(1, qty)
        item.save()
        return Response(CartSerializer(cart).data)

    def delete(self, request, item_id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.filter(id=item_id).delete()
        return Response(CartSerializer(cart).data)
