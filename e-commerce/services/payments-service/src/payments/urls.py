from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import HealthView, PaymentViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"transactions", TransactionViewSet, basename="transaction")

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
]
urlpatterns += router.urls