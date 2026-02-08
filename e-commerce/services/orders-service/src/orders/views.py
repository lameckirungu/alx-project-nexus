import requests
from decimal import Decimal
from django.conf import settings
from rest_framework.decorators import action
from rest_framework import viewsets, status
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
    
    
    @action(detail=False, methods=["post"])
    def checkout(self, request):
        """
        Create an order from cart items.

        Body:
        {
            "user_id": "<uuid>",
            "cart_id": "<uuid>"
        }
        """
        user_id = request.data.get("user_id")
        cart_id = request.data.get("cart_id")

        if not user_id or not cart_id:
            return Response({"detail": "user_id and cart_id required"}, status=400)

        cart_url = f"{settings.CART_SERVICE_URL}/api/cart/carts/{cart_id}/"
        cart_resp = requests.get(cart_url)

        if cart_resp.status_code != 200:
            return Response({"detail": "Cart not found"}, status=404)

        cart_data = cart_resp.json()
        items = cart_data.get("items", [])
        total = sum(
            Decimal(str(item["unit_price"])) * int(item["quantity"])
            for item in items
        )

        order = Order.objects.create(
            user_id=user_id,
            status="pending",
            total_amount=total,
            shipping_address=request.data.get("shipping_address", ""),
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product_id=item["product_id"],
                product_name=item["product_name"],
                unit_price=Decimal(str(item["unit_price"])),
                quantity=int(item["quantity"]),
            )

        payments_url = f"{settings.PAYMENTS_SERVICE_URL}/api/payments/payments/create_for_order/"
        payment_resp = requests.post(
            payments_url,
            json={
                "order_id": str(order.id),
                "amount": float(total),
                "method": "card",
            },
            timeout=5,
        )

        if not payment_resp.ok:
            return Response(
                {
                    "detail": "Payment creation failed",
                    "payment_status": payment_resp.status_code,
                    "payment_body": payment_resp.text,
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)     


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