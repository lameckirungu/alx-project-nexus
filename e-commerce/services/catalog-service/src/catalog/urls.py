from django.urls import path
from .views import CategoryViewSet, HealthView, ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
]
urlpatterns += router.urls