from apps.places.models import PlaceCategory
from rest_framework import serializers

__all__ = ["PlaceCategorySerializer"]


class PlaceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceCategory
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
            "path",
            "depth",
            "numchild",
        ]
