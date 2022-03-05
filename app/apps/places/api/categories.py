from apps.places.serializers import POICategorySerializer
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import viewsets

__all__ = ["POICategoryAPIViewSet"]


class POICategoryAPIViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = POICategorySerializer
    model = serializer_class.Meta.model
    queryset = model.objects.filter(is_active=True)
    pagination_class = PageNumberPaginationWithPageCounter
