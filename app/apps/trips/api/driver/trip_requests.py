from apps.trips.filters import TripRequestFilter
from apps.trips.serializers import (  # TripRequestSearchSerializer,
    TripRequestDetailSerializer,
    TripRequestListSerializer,
)
from apps.trips.services import TripRequestService
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django_filters.rest_framework import DjangoFilterBackend
from packages.math.metric_buffer import with_metric_buffer
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import permissions, viewsets

# from rest_framework.decorators import action
# from rest_framework.response import Response

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

    def get_serializer_class(self):
        # if self.action == "search":
        #     return TripRequestSearchSerializer
        if self.request.query_params.get("return_routes", False) == "true":
            return TripRequestDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = self.model.objects.active()
        return qs.prefetch_related("trip__waypoints")

    def filter_queryset(self, qs):

        lon = self.request.query_params.get("lon")
        lat = self.request.query_params.get("lat")
        radius = self.request.query_params.get("radius")

        location = None
        area = None

        if lon and lat:
            location = Point(float(lon), float(lat), srid=4326)

            # TODO: move to QuerySet
            qs = qs.annotate(distance=Distance("starting_point", location)).order_by(
                "distance"
            )

            if radius:
                area = with_metric_buffer(location, int(radius) * 1000)
                qs = qs.filter(starting_point__coveredby=area)

        qs = super().filter_queryset(qs)

        TripRequestService.log_trip_request_search(
            user_session=self.request.query_params.get("user_session"),
            point=location,
            area=area,
            radius=radius,
            number_of_people=self.request.query_params.get("number_of_people"),
            with_pets=self.request.query_params.get("with_pets"),
            luggage_size=self.request.query_params.get("luggage_size"),
            spoken_languages=self.request.query_params.get("spoken_languages"),
            results=qs,
        )

        return qs

    # @action(detail=False, methods=["post"], url_path="search")
    # def search(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     return Response()
