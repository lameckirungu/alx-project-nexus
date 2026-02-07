from .models import CartItem, Cart
from .serializers import CartItemSerializer, CartSerializer
from rest_framework import viewsets
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
    
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.select_related("cart").all()
    serializer_class = CartItemSerializer