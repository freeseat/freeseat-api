from apps.trips.enums import LuggageSize
from apps.trips.filters import TripRequestFilter
from apps.trips.serializers import (
    TripRequestSearchSerializer,
    TripRequestDetailSerializer,
    TripRequestListSerializer,
)
from apps.trips.services import TripRequestService
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models.expressions import Q, RawSQL
from django_filters.rest_framework import DjangoFilterBackend
from packages.math.metric_buffer import with_metric_buffer
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from geojson.geometry import LineString


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
        if self.request.query_params.get("return_routes", False) == "true":
            return TripRequestDetailSerializer

        return {
            "search": TripRequestSearchSerializer,
            "detail": TripRequestDetailSerializer,
        }.get(self.action, super().get_serializer_class())

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

    @action(detail=False, methods=["post"], url_path="search")
    def search(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        qs = self.get_queryset()

        driver_route = data.get("route")
        max_deviation_meters = data.get("max_deviation") * 1000
        spoken_languages = data.get("spoken_languages")
        number_of_people = data.get("number_of_people")
        luggage_size = data.get("luggage_size")

        with_pets = data.get("with_pets")
        if not with_pets:
            qs = qs.exclude(with_pets=True)

        if luggage_size == LuggageSize.CARGO:
            qs = qs.filter(luggage_size=luggage_size)
        else:
            qs = qs.filter(luggage_size__lte=luggage_size)

        qs = qs.filter(
            number_of_people__lte=number_of_people,
            spoken_languages__in=spoken_languages,
        )

        allow_partial_trip = qs.filter(allow_partial_trip=True)

        full_trip_only = qs.difference(allow_partial_trip)

        allow_partial_trip = list(allow_partial_trip.values_list("id", flat=True))
        full_trip_only = list(full_trip_only.values_list("id", flat=True))

        driver_route = LineString(driver_route)
        print(driver_route)

        qs = qs.filter(
            Q(trip_id__in=RawSQL(f"SELECT * FROM match_partial_trips(ARRAY[{allow_partial_trip}]::uuid[], %s, {max_deviation_meters})", [str(driver_route)])) |
            Q(trip_id__in=RawSQL(f"SELECT * FROM match_entire_trips(ARRAY[{full_trip_only}]::uuid[], %s, {max_deviation_meters})", [str(driver_route)]))
        )

        serializer_class = self.get_serializer_class()

        return Response(serializer_class(qs, many=True).data)
