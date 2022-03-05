from apps.places.serializers import PointOfInterestSerializer
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import viewsets

__all__ = ["PointOfInterestAPIViewSet"]


class PointOfInterestAPIViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PointOfInterestSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.filter(is_active=True)
    pagination_class = PageNumberPaginationWithPageCounter
