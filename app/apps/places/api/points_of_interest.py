from apps.places.serializers import (
    PointOfInterestDetailSerializer,
    PointOfInterestListSerializer,
)
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import viewsets

__all__ = ["PointOfInterestAPIViewSet"]


class PointOfInterestAPIViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PointOfInterestDetailSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.filter(is_active=True)
    pagination_class = PageNumberPaginationWithPageCounter

    def get_serializer_class(self):
        if self.action == "list":
            return PointOfInterestListSerializer
        return self.serializer_class
