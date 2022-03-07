from apps.accounts.models import UserSession
from apps.trips.enums import TripState
from apps.trips.serializers import (
    TripRequestCreateSerializer,
    TripRequestExtendSerializer,
    TripRequestListSerializer,
    TripRequestPassengerSerializer,
    TripRequestStateChangeSerializer,
)
from apps.trips.services import TripRequestService
from django.db import transaction
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

__all__ = ["PassengerTripRequestAPIViewSet"]


class PassengerTripRequestAPIViewSet(
    mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet
):
    """
    Returns a list of requested trips.
    Note: a query parameter user_session should be passed.
    """

    serializer_class = TripRequestListSerializer
    model = serializer_class.Meta.model
    pagination_class = PageNumberPaginationWithPageCounter
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        return {
            "create": TripRequestCreateSerializer,
            "cancel_trip_request": TripRequestStateChangeSerializer,
            "complete_trip_request": TripRequestStateChangeSerializer,
            "extend_trip_request": TripRequestExtendSerializer,
        }.get(self.action, TripRequestPassengerSerializer)

    def get_queryset(self):
        qs = self.model.objects.filter(state=TripState.ACTIVE)

        if self.action == "list":
            user_session_id = self.request.query_params.get("user_session")

            try:
                user_session = UserSession.objects.get(id=user_session_id)
                qs = qs.filter(user_session=user_session)
            except UserSession.DoesNotExist:
                return qs.none()

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

    @transaction.atomic
    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_trip_request(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        TripRequestService.cancel_requested_trip(instance, serializer.validated_data)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(detail=True, methods=["post"], url_path="complete")
    def complete_trip_request(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        TripRequestService.complete_requested_trip(instance, serializer.validated_data)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(detail=True, methods=["post"], url_path="extend")
    def extend_trip_request(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        trip_request = TripRequestService.extend_trip_request(
            instance, serializer.validated_data.get("extend_for")
        )

        return Response(TripRequestPassengerSerializer(trip_request).data)
