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
            "url",
            "name_en",
            "name_ru",
            "name_uk",
            "name_pl",
            "name_de",
            "description_en",
            "description_ru",
            "description_uk",
            "description_pl",
            "description_de",
            "point",
            "category",
        ]
