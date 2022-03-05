from apps.accounts.models import UserSession
from apps.trips.serializers import (
    TripRequestCreateSerializer,
    TripRequestPrivateSerializer,
    TripRequestPublicSerializer,
)
from apps.trips.services import TripRequestService
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_filters import fields, filters, filterset
from django_filters.rest_framework import DjangoFilterBackend
from packages.math.metric_buffer import with_metric_buffer
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

__all__ = ["TripRequestsAPIViewSet"]


class TripRequestsFilter(filterset.FilterSet):
    user_session = filters.ModelChoiceFilter(
        method="filter_by_user_session",
        label=_("user session"),
        queryset=UserSession.objects.all(),
    )

    def filter_by_user_session(self, queryset, name, value):
        return queryset

    spoken_languages = filters.BaseCSVFilter(
        method="filter_by_spoken_languages",
        label=_("spoken languages"),
        widget=fields.CSVWidget,
    )

    def filter_by_spoken_languages(self, queryset, name, value):
        return queryset.filter(spoken_languages__code__in=value).distinct()

    with_pets = filters.BooleanFilter(
        method="filter_by_pets",
        label=_("with pets"),
    )

    def filter_by_pets(self, queryset, name, value):
        if value:
            return queryset
        return queryset.exclude(with_pets=True)

    number_of_people = filters.NumberFilter(
        label=_("number of people"),
        lookup_expr="lte",
    )

    luggage_size = filters.NumberFilter(
        label=_("luggage size"),
        method="filter_by_luggage_size",
    )

    def filter_by_luggage_size(self, queryset, name, value):
        if value == self.Meta.model.LuggageSize.CARGO:
            return queryset.filter(luggage_size=value)
        return queryset.filter(luggage_size__lte=value)

    lon = filters.NumberFilter(
        label=_("longitude"),
        method="filter_by_lon",
    )

    def filter_by_lon(self, queryset, name, value):
        return queryset

    lat = filters.NumberFilter(
        label=_("latitude"),
        method="filter_by_lat",
    )

    def filter_by_lat(self, queryset, name, value):
        return queryset

    radius = filters.NumberFilter(
        label=_("radius"),
        method="filter_by_radius",
    )

    def filter_by_radius(self, queryset, name, value):
        return queryset

    page_size = filters.NumberFilter(
        label=_("page size"),
        method="filter_by_page_size",
    )

    def filter_by_page_size(self, queryset, name, value):
        return queryset

    class Meta:
        model = TripRequestPublicSerializer.Meta.model
        fields = [
            "user_session",
            "spoken_languages",
            "with_pets",
            "number_of_people",
            "with_pets",
            "luggage_size",
            "lon",
            "lat",
            "radius",
        ]


class TripRequestsAPIViewSet(viewsets.ModelViewSet):
    """
    Returns a list of requested trips.

        This endpoint is used in 2 scenarios:

        1. Retrieving a list of requested trips for user session.
        In that case query parameter user_session should be passed.

        2. Search through requested trips by other users.
        In that case query parameter user_session should be omitted and
        other parameters used for filtering instead.

        Filtering by lon and lat:

        1. In case lon, lat and radius (in km) are provided, the result
        will be limited to trip requests that start in a given area.

        2. In case only lon and lat are provided, only 10 nearest results
        will be returned.
    """

    serializer_class = TripRequestPublicSerializer
    model = serializer_class.Meta.model
    pagination_class = PageNumberPaginationWithPageCounter
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_class = TripRequestsFilter
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        now = timezone.now()
        past_24_hours = now - timezone.timedelta(hours=24)

        qs = self.model.objects.filter(
            state=self.model.TripRequestState.ACTIVE,
            last_active_at__gte=past_24_hours,
        )

        if self.request.user.is_authenticated:
            qs = qs.filter(created_by=self.request.user)

        elif user_session_id := self.request.query_params.get("user_session"):
            try:
                user_session = UserSession.objects.get(id=user_session_id)
                user_session.last_active_at = now
                user_session.save(update_fields=["last_active_at"])
                qs = qs.filter(user_session=user_session)
            except UserSession.DoesNotExist:
                return qs

        else:
            lon = self.request.query_params.get("lon")
            lat = self.request.query_params.get("lat")
            radius = self.request.query_params.get("radius")

            if lon and lat:
                location = Point(float(lon), float(lat), srid=4326)
                qs = qs.annotate(
                    distance=Distance("starting_point", location)
                ).order_by("distance")

                if radius:
                    area = with_metric_buffer(
                        location, int(radius) * 1000, map_srid=4326
                    )
                    qs = qs.filter(starting_point__coveredby=area)

            return qs

        if qs:
            qs.update(last_active_at=now)

        return qs.prefetch_related("waypoints")

    def get_serializer_class(self):
        if self.action == "create":
            return TripRequestCreateSerializer
        if (
            self.request.user.is_authenticated
            or UserSession.objects.filter(
                id=self.request.query_params.get("user_session")
            ).exists()
            or self.action in ["update", "partial_update"]
        ):
            return TripRequestPrivateSerializer
        return super().get_serializer_class()

    def perform_update(self, serializer):
        TripRequestService.update_requested_trip(
            serializer.instance, serializer.validated_data
        )

    def perform_create(self, serializer):
        TripRequestService.request_trip(serializer.validated_data)

    def perform_destroy(self, instance):
        instance.state = self.model.TripRequestState.CANCELLED
        instance.save(update_fields=["state"])

    @action(detail=True, methods=["post"], url_path="complete")
    def complete_trip_request(self, request, *args, **kwargs):
        trip_request = self.get_object()
        trip_request.state = self.model.TripRequestState.COMPLETED
        trip_request.save(update_fields=["state"])
        return Response()
