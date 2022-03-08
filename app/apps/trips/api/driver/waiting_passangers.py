from apps.trips.serializers import (
    TripRequestListSerializer,
    TripRequestStartingPointSerializer,
)
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import viewsets

__all__ = ["WaitingPassengerViewSet"]


class WaitingPassengerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TripRequestListSerializer
    model = TripRequestListSerializer.Meta.model
    pagination_class = PageNumberPaginationWithPageCounter

    def get_queryset(self):
        return self.model.objects.active()

    def get_serializer_class(self):
        if self.action == "list":
            return TripRequestStartingPointSerializer
        return super().get_serializer_class()
