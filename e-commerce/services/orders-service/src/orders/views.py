from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class HealthView(APIView):
    @extend_schema(
        summary="Health check",
        description="Returns service health status for the orders service.",
        responses={200: {"type": "object", "example": {"status": "ok", "service": "orders"}}},
    )
    def get(self, request):
        return Response({"status": "ok", "service": "orders"})


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders.
    
    Provides CRUD operations for orders including creation, retrieval, updates, and deletion.
    """
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer

    @extend_schema(
        summary="List all orders",
        description="Retrieve a paginated list of all orders.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new order",
        description="Create a new order with items.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve an order",
        description="Get details of a specific order by ID.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update an order",
        description="Update order status or other details.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an order",
        description="Delete a specific order by ID.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing order items.
    
    Provides CRUD operations for items within orders.
    """
    queryset = OrderItem.objects.select_related("order").all()
    serializer_class = OrderItemSerializer

    @extend_schema(
        summary="List all order items",
        description="Retrieve a paginated list of all order items.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create an order item",
        description="Add a new item to an order.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)