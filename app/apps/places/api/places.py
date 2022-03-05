from apps.places.serializers import PlaceSerializer
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import viewsets

__all__ = ["PlaceAPIViewSet"]


class PlaceAPIViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlaceSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.filter(is_active=True)
    pagination_class = PageNumberPaginationWithPageCounter
