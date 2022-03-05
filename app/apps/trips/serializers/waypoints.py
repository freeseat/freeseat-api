from apps.trips.models import WayPoint
from rest_framework import serializers

__all__ = ["WayPointSerializer"]


class WayPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WayPoint
        fields = ["order", "point"]
