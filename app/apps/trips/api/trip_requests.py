from apps.accounts.models import UserSession
from apps.trips.serializers import (
    TripRequestCreateSerializer,
    TripRequestPrivateSerializer,
    TripRequestPublicSerializer,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_filters import fields, filters, filterset
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

__all__ = ["TripRequestsAPIViewSet"]


class TripRequestsFilter(filterset.FilterSet):
    spoken_languages = filters.BaseCSVFilter(
        method="filter_by_spoken_languages",
        label=_("spoken languages"),
        widget=fields.CSVWidget,
    )

    def filter_by_spoken_languages(self, queryset, name, value):
        return queryset.filter(spoken_languages__code__in=value)

    number_of_people = filters.NumberFilter(
        label=_("number of people"),
        lookup_expr="lte",
    )

    luggage_size = filters.NumberFilter(
        label=_("luggage size"),
        lookup_expr="lte",
    )

    class Meta:
        model = TripRequestPublicSerializer.Meta.model
        fields = [
            "spoken_languages",
            "number_of_people",
            "with_pets",
            "luggage_size",
        ]


class TripRequestsAPIViewSet(viewsets.ModelViewSet):
    serializer_class = TripRequestPublicSerializer
    model = serializer_class.Meta.model
    pagination_class = PageNumberPagination
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_class = TripRequestsFilter

    def get_queryset(self):
        qs = self.model.objects.all()

        if self.request.user.is_authenticated:
            qs = qs.filter(created_by=self.request.user)

        elif user_session := self.request.query_params.get("user_session"):
            user_session.last_active_at = timezone.now()
            user_session.save(update_fields=["last_active_at"])

            qs = qs.filter(user_session=user_session)

        else:
            return qs

        if qs:
            qs.update(last_active_at=timezone.now())

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

    def perform_destroy(self, instance):
        instance.state = self.model.TripState.CANCELLED
        instance.save(update_fields=["state"])

    @action(detail=True, methods=["post"], url_path="complete")
    def complete_trip_request(self, request, *args, **kwargs):
        trip_request = self.get_object()
        trip_request.state = self.model.TripState.COMPLETED
        trip_request.save(update_fields=["state"])
        return Response()
