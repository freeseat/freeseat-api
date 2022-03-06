from apps.trips.models import TripRequest
from rest_framework import serializers

__all__ = ["TripRequestStartingPointSerializer"]


class TripRequestStartingPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripRequest
        fields = [
            "id",
            "starting_point",
            "number_of_people",
        ]
