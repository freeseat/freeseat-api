from apps.operations.serializers import MessageSerializer
from rest_framework import generics

__all__ = ["MessageCreateAPIView"]


class MessageCreateAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
