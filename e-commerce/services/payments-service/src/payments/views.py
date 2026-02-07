from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .models import Payment, Transaction
from .serializers import PaymentSerializer, TransactionSerializer


class HealthView(APIView):
    @extend_schema(
        summary="Health check",
        description="Returns service health status for the payments service.",
        responses={200: {"type": "object", "example": {"status": "ok", "service": "payments"}}},
    )
    def get(self, request):
        return Response({"status": "ok", "service": "payments"})


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing payments.
    """
    queryset = Payment.objects.all().order_by("-created_at")
    serializer_class = PaymentSerializer

    @extend_schema(summary="List payments", description="Retrieve all payments.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Create payment", description="Create a new payment record.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="Retrieve payment", description="Retrieve a payment by ID.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing payment transactions.
    """
    queryset = Transaction.objects.select_related("payment").all()
    serializer_class = TransactionSerializer

    @extend_schema(summary="List transactions", description="Retrieve all transactions.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Create transaction", description="Create a new transaction.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
