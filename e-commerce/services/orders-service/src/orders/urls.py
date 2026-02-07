from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, OrderItemViewSet, HealthView

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"items", OrderItemViewSet, basename="order-item")

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
]
urlpatterns += router.urls