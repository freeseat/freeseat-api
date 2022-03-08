from apps.accounts.models import UserSession
from apps.trips.models import TripRequest
from apps.trips.serializers.waypoints import WayPointSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.validators import ValidationError
from rest_framework_gis.fields import GeometryField

__all__ = [
    "TripRequestListSerializer",
    "TripRequestDetailSerializer",
    "TripRequestCreateSerializer",
    "TripRequestStateChangeSerializer",
    "TripRequestExtendSerializer",
    "TripRequestPassengerSerializer",
]


class TripRequestListSerializer(serializers.ModelSerializer):
    waypoints = WayPointSerializer(source="trip.waypoints", many=True, allow_null=True)
    route_length = serializers.FloatField(source="trip.route_length", allow_null=True)
    route = GeometryField(
        write_only=True, source="trip.route", allow_null=True, required=False, default=None,
    )
    distance_in_km = serializers.FloatField(
        source="distance.km", read_only=True, default=None
    )

    class Meta:
        model = TripRequest
        read_only_fields = ["id", "updated_at", "distance_in_km", "active_until"]
        fields = read_only_fields + [
            "spoken_languages",
            "number_of_people",
            "with_pets",
            "comment",
            "phone_number",
            "luggage_size",
            "waypoints",
            "route_length",
            "route",
            "allow_partial_trip",
        ]


class TripRequestDetailSerializer(TripRequestListSerializer):
    route = GeometryField(source="trip.route", allow_null=True)


class TripRequestCreateSerializer(TripRequestListSerializer):
    user_session = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=UserSession.objects.all(), required=False
    )
    active_for = serializers.IntegerField(required=False)

    def validate(self, attrs):
        if (user := self.context.get("request").user) and user.is_authenticated:
            attrs["created_by"] = user
        else:
            if not attrs.get("user_session"):
                raise ValidationError({"user_session": [_("This field is required.")]})

        return attrs

    class Meta(TripRequestListSerializer.Meta):
        fields = TripRequestListSerializer.Meta.fields + ["user_session", "active_for"]


class TripRequestStateChangeSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(required=False)
    result = serializers.CharField(source="report.result", required=False)
    satisfaction_rate = serializers.IntegerField(
        source="report.satisfaction_rate", required=False
    )

    def validate_user_session(self, user_session):
        if self.instance.user_session != user_session:
            raise PermissionDenied
        return user_session

    class Meta:
        model = TripRequest
        fields = [
            "user_session",
            "result",
            "satisfaction_rate",
            "comment",
        ]


class TripRequestExtendSerializer(serializers.ModelSerializer):
    extend_for = serializers.IntegerField()

    def validate_user_session(self, user_session):
        if self.instance.user_session != user_session:
            raise PermissionDenied
        return user_session

    class Meta:
        model = TripRequest
        fields = [
            "user_session",
            "extend_for",
        ]


class TripRequestPassengerSerializer(TripRequestDetailSerializer):
    pass
