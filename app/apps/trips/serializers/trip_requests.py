from apps.accounts.models import UserSession
from apps.trips.models import TripRequest
from apps.trips.serializers.waypoints import WayPointSerializer
from django.contrib.gis.geos import Point
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import ValidationError

__all__ = [
    "TripRequestPublicSerializer",
    "TripRequestPrivateSerializer",
    "TripRequestCreateSerializer",
]


class TripRequestPublicSerializer(serializers.ModelSerializer):
    waypoints = WayPointSerializer(many=True)

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
            "last_active_at",
        ]
        fields = read_only_fields + [
            "spoken_languages",
            "number_of_people",
            "with_pets",
            "comment",
            "luggage_size",
            "waypoints",
        ]

    @transaction.atomic
    def create(self, validated_data):
        waypoints = validated_data.pop("waypoints")

        trip_request = super().create(validated_data)

        for waypoint in waypoints:
            WayPointSerializer.Meta.model.objects.create(
                trip_request=trip_request,
                order=waypoint.get("order"),
                point=Point(
                    *waypoint.get("point").get("coords"),
                ),
            )

        return trip_request


class TripRequestPrivateSerializer(TripRequestPublicSerializer):
    class Meta(TripRequestPublicSerializer.Meta):
        fields = TripRequestPublicSerializer.Meta.fields + ["id"]


class TripRequestCreateSerializer(TripRequestPrivateSerializer):
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

    class Meta(TripRequestPrivateSerializer.Meta):
        fields = TripRequestPrivateSerializer.Meta.fields + ["user_session"]
