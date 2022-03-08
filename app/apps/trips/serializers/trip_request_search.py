from apps.trips.models import TripRequest
from apps.trips.serializers.waypoints import WayPointSerializer
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

__all__ = ["TripRequestSearchSerializer"]


class TripRequestSearchSerializer(serializers.ModelSerializer):
    max_deviation = serializers.IntegerField()
    # waypoints = WayPointSerializer(many=True)
    route = GeometryField()
    page_size = serializers.IntegerField(default=20)
    disable_pagination = serializers.BooleanField(default=False)

    class Meta:
        model = TripRequest
        fields = [
            "user_session",
            "spoken_languages",
            "with_pets",
            "number_of_people",
            "luggage_size",
            # "waypoints",
            "route",
            "max_deviation",
            "page_size",
            "disable_pagination",
        ]
