from apps.accounts.models import UserSession
from apps.accounts.serializers import ContactInformationSerializer
from apps.trips.models import TripProposal
from apps.trips.serializers.waypoints import WayPointSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.validators import ValidationError
from rest_framework_gis.fields import GeometryField

__all__ = [
    "TripProposalListSerializer",
    "TripProposalCreateSerializer",
    "TripProposalStateChangeSerializer",
]


class TripProposalListSerializer(serializers.ModelSerializer):
    waypoints = WayPointSerializer(source="trip.waypoints", many=True, allow_null=True)
    route_length = serializers.FloatField(source="trip.route_length", allow_null=True)
    route = GeometryField(write_only=True, source="trip.route", allow_null=True)
    distance_in_km = serializers.FloatField(
        source="distance.km", read_only=True, default=None
    )
    contact_information = ContactInformationSerializer()

    class Meta:
        model = TripProposal
        read_only_fields = [
            "id",
            "distance_in_km",
        ]
        fields = read_only_fields + [
            "spoken_languages",
            "number_of_seats",
            "pets_allowed",
            "comment",
            "contact_information",
            "luggage_carrier_size",
            "waypoints",
            "route_length",
            "route",
        ]


class TripProposalCreateSerializer(TripProposalListSerializer):
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

    class Meta(TripProposalListSerializer.Meta):
        fields = TripProposalListSerializer.Meta.fields + ["user_session"]


class TripProposalStateChangeSerializer(serializers.ModelSerializer):
    def validate_user_session(self, user_session):
        if self.instance.user_session != user_session:
            raise PermissionDenied
        return user_session

    class Meta:
        model = TripProposal
        fields = [
            "user_session",
        ]
