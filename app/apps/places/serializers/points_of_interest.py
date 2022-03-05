from apps.places.models import PointOfInterest
from rest_framework import serializers

__all__ = ["PointOfInterestSerializer"]


class PointOfInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfInterest
        fields = [
            "id",
            "name_en",
            "name_ru",
            "name_uk",
            "name_pl",
            "description_en",
            "description_ru",
            "description_uk",
            "description_pl",
            "point",
            "category",
        ]
