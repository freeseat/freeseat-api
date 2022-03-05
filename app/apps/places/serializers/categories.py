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
            "description_en",
            "description_ru",
            "description_uk",
            "description_pl",
            "path",
            "depth",
            "numchild",
        ]
