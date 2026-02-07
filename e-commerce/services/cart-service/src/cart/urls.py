from django.urls import path
from .views import HealthView, CartViewSet, CartItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename="cart")
router.register(r'items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('health/', HealthView.as_view(), name='health'),
]

urlpatterns += router.urls