from .models import CartItem, Cart
from .serializers import CartItemSerializer, CartSerializer
from .permissions import IsOwner
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

class HealthView(APIView):
    @extend_schema(
            summary="Health check",
            description="Returns service health status for the cart service.",
            responses={200: {"type": "object", "example": {"status": "ok", "service": "cart"}}},
    )
    def get(self, request):
        return Response({"status": "ok", "service": "cart"})
    
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by("-updated_at")
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user_id = str(getattr(self.request.user, "id", ""))
        return Cart.objects.filter(user_id=user_id).order_by("-updated_at")

    def perform_create(self, serializer):
        serializer.save(user_id=str(getattr(self.request.user, "id", "")))
    
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.select_related("cart").all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user_id = str(getattr(self.request.user, "id", ""))
        return CartItem.objects.select_related("cart").filter(cart__user_id=user_id)

    def perform_create(self, serializer):
        cart = serializer.validated_data.get("cart")
        user_id = str(getattr(self.request.user, "id", ""))
        if str(cart.user_id) != user_id:
            raise permissions.PermissionDenied("Not allowed to modify this cart")
        serializer.save()