from apps.places.models import PointOfInterest
from apps.places.serializers.categories import POICategorySerializer
from rest_framework import serializers

__all__ = ["PointOfInterestListSerializer", "PointOfInterestDetailSerializer"]


class PointOfInterestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfInterest
        fields = [
            "id",
            "category",
            "point",
        ]


class PointOfInterestDetailSerializer(serializers.ModelSerializer):
    category = POICategorySerializer()

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
