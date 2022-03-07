from apps.trips.models import WayPoint
from rest_framework import serializers

__all__ = ["WayPointSerializer"]


class WayPointSerializer(serializers.ModelSerializer):
    country = serializers.CharField(read_only=True)

    class Meta:
        model = WayPoint
        fields = ["order", "point", "country"]
