from apps.trips.filters import TripRequestFilter
from apps.trips.serializers import TripRequestListSerializer
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django_filters.rest_framework import DjangoFilterBackend
from packages.math.metric_buffer import with_metric_buffer
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import permissions, viewsets

__all__ = ["DriverTripRequestAPIViewSet"]


class DriverTripRequestAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Returns a list of requested trips.
        Filtering by lon and lat:

        1. In case lon, lat and radius (in km) are provided, the result
        will be limited to trip requests that start in a given area.

        2. In case only lon and lat are provided, only 10 nearest results
        will be returned.
    """

    serializer_class = TripRequestListSerializer
    model = serializer_class.Meta.model
    pagination_class = PageNumberPaginationWithPageCounter
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_class = TripRequestFilter
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = self.model.objects.active()

        lon = self.request.query_params.get("lon")
        lat = self.request.query_params.get("lat")
        radius = self.request.query_params.get("radius")

        if lon and lat:
            location = Point(float(lon), float(lat), srid=4326)
            qs = qs.annotate(distance=Distance("starting_point", location)).order_by(
                "distance"
            )

            if radius:
                area = with_metric_buffer(location, int(radius) * 1000, map_srid=4326)
                qs = qs.filter(starting_point__coveredby=area)

        return qs.prefetch_related("trip__waypoints")
