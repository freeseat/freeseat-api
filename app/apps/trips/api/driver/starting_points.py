from apps.trips.serializers import (
    TripRequestListSerializer,
    TripRequestStartingPointSerializer,
)
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import viewsets

__all__ = ["TripRequestStartingPointViewSet"]


class TripRequestStartingPointViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TripRequestListSerializer
    model = TripRequestListSerializer.Meta.model
    queryset = model.objects.active()
    pagination_class = PageNumberPaginationWithPageCounter

    def get_serializer_class(self):
        if self.action == "list":
            return TripRequestStartingPointSerializer
        return super().get_serializer_class()
