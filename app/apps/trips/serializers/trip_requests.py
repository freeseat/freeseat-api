from apps.accounts.models import UserSession
from apps.trips.models import TripRequest
from apps.trips.serializers.waypoints import WayPointSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework_gis.fields import GeometryField

__all__ = [
    "TripRequestListSerializer",
    "TripRequestCreateSerializer",
]


class TripRequestListSerializer(serializers.ModelSerializer):
    waypoints = WayPointSerializer(source="trip.waypoints", many=True, allow_null=True)
    route_length = serializers.FloatField(source="trip.route_length", allow_null=True)
    route = GeometryField(write_only=True, source="trip.route", allow_null=True)
    distance_in_km = serializers.FloatField(
        source="distance.km", read_only=True, default=None
    )

    def validate_waypoints(self, waypoints):
        if len(waypoints) < 2:
            raise ValidationError(
                {
                    "waypoints": [_("This list should contain at least 2 points.")],
                }
            )

        return waypoints

    class Meta:
        model = TripRequest
        read_only_fields = [
            "id",
            "last_active_at",
            "distance_in_km",
        ]
        fields = read_only_fields + [
            "spoken_languages",
            "number_of_people",
            "with_pets",
            "comment",
            "luggage_size",
            "waypoints",
            "route_length",
            "route",
            "allow_partial_trip",
        ]


class TripRequestCreateSerializer(TripRequestListSerializer):
    user_session = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=UserSession.objects.all(), required=False
    )

    def validate(self, attrs):
        if (user := self.context.get("request").user) and user.is_authenticated:
            attrs["created_by"] = user
        else:
            if not attrs.get("user_session"):
                raise ValidationError({"user_session": [_("This field is required.")]})

        return attrs

    class Meta(TripRequestListSerializer.Meta):
        fields = TripRequestListSerializer.Meta.fields + ["user_session"]
