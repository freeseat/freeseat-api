from apps.accounts.serializers import UserSessionSerializer
from rest_framework import generics

__all__ = ["UserSessionCreateAPIView"]


class UserSessionCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSessionSerializer
