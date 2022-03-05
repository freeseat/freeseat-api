from apps.places.models import POICategory
from rest_framework import serializers

__all__ = ["POICategorySerializer"]


class POICategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = POICategory
        fields = [
            "id",
            "name_en",
            "name_ru",
            "name_uk",
            "name_pl",
        ]
