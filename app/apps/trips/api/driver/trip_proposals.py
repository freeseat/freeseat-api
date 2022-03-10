from apps.accounts.models import UserSession
from apps.trips.serializers import (
    TripProposalCreateSerializer,
    TripProposalListSerializer,
    TripProposalStateChangeSerializer,
)
from apps.trips.services import TripProposalService
from django.db import transaction
from django.utils import timezone
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

__all__ = ["DriverTripProposalAPIViewSet"]


class DriverTripProposalAPIViewSet(
    mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet
):
    """
    Returns a list of proposed trips.
    Note: a query parameter user_session should be passed.
    """

    serializer_class = TripProposalListSerializer
    model = serializer_class.Meta.model
    pagination_class = PageNumberPaginationWithPageCounter
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        return {
            "create": TripProposalCreateSerializer,
            "cancel_trip_proposal": TripProposalStateChangeSerializer,
            "complete_trip_proposal": TripProposalStateChangeSerializer,
        }.get(self.action, TripProposalCreateSerializer)

    def get_queryset(self):
        now = timezone.now()

        qs = self.model.objects.active()

        if self.action == "list":
            user_session_id = self.request.query_params.get("user_session")

            try:
                user_session = UserSession.objects.get(id=user_session_id)
                user_session.last_active_at = now
                user_session.save(update_fields=["last_active_at"])
                qs = qs.filter(user_session=user_session)
            except UserSession.DoesNotExist:
                return qs.none()

        return qs.prefetch_related("trip__waypoints")

    def perform_update(self, serializer):
        return TripProposalService.update_proposed_trip(
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
        return TripProposalService.propose_trip(serializer.validated_data)

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
    def cancel_trip_proposal(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        TripProposalService.cancel_requested_trip(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(detail=True, methods=["post"], url_path="complete")
    def complete_trip_proposal(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        TripProposalService.complete_proposed_trip(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
