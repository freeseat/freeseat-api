from apps.trips.serializers import TripRequestCreateSerializer, TripRequestSerializer
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

__all__ = ["TripRequestsAPIViewSet"]


class TripRequestsAPIViewSet(viewsets.ModelViewSet):
    serializer_class = TripRequestSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        qs = self.serializer_class.Meta.model.objects.all()

        if self.request.user.is_authenticated:
            qs = qs.filter(created_by=self.request.user)

        elif user_session := self.request.query_params.get("user_session"):
            qs = qs.filter(user_session=user_session)

        else:
            return qs.none()

        if qs:
            qs.update(last_active_at=timezone.now())

        return qs.prefetch_related("waypoints")

    def get_serializer_class(self):
        if self.action == "create":
            return TripRequestCreateSerializer
        return super().get_serializer_class()
