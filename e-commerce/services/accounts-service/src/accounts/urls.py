from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import HealthView, ProfileViewSet, RegisterView, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"profiles", ProfileViewSet, basename="profile")

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("register/", RegisterView.as_view(), name="register"),
]

urlpatterns += router.urls