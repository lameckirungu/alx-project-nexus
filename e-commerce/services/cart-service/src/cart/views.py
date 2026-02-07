from .models import CartItem, Cart
from .serializers import CartItemSerializer, CartSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok", "service": "cart"})
    
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by("-updated_at")
    serializer_class = CartSerializer
    
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.select_related("cart").all()
    serializer_class = CartItemSerializer