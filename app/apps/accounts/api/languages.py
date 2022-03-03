from apps.accounts.serializers import LanguageSerializer
from rest_framework import generics

__all__ = ["LanguageListAPIView"]


class LanguageListAPIView(generics.ListAPIView):
    serializer_class = LanguageSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
