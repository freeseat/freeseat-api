from apps.accounts.models import UserSession
from apps.trips.filters import TripRequestFilter
from apps.trips.serializers import (
    TripRequestCreateSerializer,
    TripRequestPrivateSerializer,
    TripRequestPublicSerializer,
)
from apps.trips.services import TripRequestService
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from packages.math.metric_buffer import with_metric_buffer
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

__all__ = ["TripRequestAPIViewSet"]


class TripRequestAPIViewSet(viewsets.ModelViewSet):
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
    filter_class = TripRequestFilter
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        serializer_class = {
            "create": TripRequestCreateSerializer,
            "update": TripRequestPrivateSerializer,
            "partial_update": TripRequestPrivateSerializer,
        }.get(self.action, self.serializer_class)

        # TODO: refactor after splitting APIs
        if (
            self.request.user.is_authenticated
            or UserSession.objects.filter(
                id=self.request.query_params.get("user_session")
            ).exists()
        ):
            serializer_class = TripRequestPrivateSerializer

        return serializer_class

    def get_queryset(self):
        now = timezone.now()

        qs = self.model.objects.active()

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
            TripRequestService.actualize_trip_requests_list(qs)

        return qs.prefetch_related("trip__waypoints")

    def perform_update(self, serializer):
        return TripRequestService.update_requested_trip(
            serializer.instance, serializer.validated_data
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_update(serializer)
        serializer = self.get_serializer(instance)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_create(self, serializer):
        return TripRequestService.request_trip(serializer.validated_data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_create(serializer)
        serializer = self.get_serializer(instance)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_destroy(self, instance):
        TripRequestService.cancel_requested_trip(instance)

    @transaction.atomic
    @action(detail=True, methods=["post"], url_path="complete")
    def complete_trip_request(self, request, *args, **kwargs):
        instance = self.get_object()
        TripRequestService.cancel_requested_trip(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
