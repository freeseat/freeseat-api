from apps.trips.serializers import (
    TripRequestPublicSerializer,
    TripRequestStartingPointSerializer,
)
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import viewsets

__all__ = ["TripRequestStartingPointViewSet"]


class TripRequestStartingPointViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TripRequestPublicSerializer
    model = TripRequestPublicSerializer.Meta.model
    queryset = model.objects.active()
    pagination_class = PageNumberPaginationWithPageCounter

    def get_serializer_class(self):
        if self.action == "list":
            return TripRequestStartingPointSerializer
        return super().get_serializer_class()
