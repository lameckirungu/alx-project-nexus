from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import UserSerializer, RegisterSerializer, ProfileSerializer

User = get_user_model()

class HealthView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Profiles are created automatically when a user is created."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )