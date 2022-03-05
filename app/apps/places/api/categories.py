from apps.places.serializers import PlaceCategorySerializer
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import viewsets

__all__ = ["PlaceCategoryAPIViewSet"]


class PlaceCategoryAPIViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlaceCategorySerializer
    model = serializer_class.Meta.model
    queryset = model.objects.filter(is_active=True)
    pagination_class = PageNumberPaginationWithPageCounter
