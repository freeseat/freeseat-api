from apps.trips.models import WayPoint
from rest_framework import serializers

__all__ = ["WayPointSerializer"]


class WayPointSerializer(serializers.ModelSerializer):
    point = serializers.ListField(source="point.coords")

    class Meta:
        model = WayPoint
        fields = ["order", "point"]
