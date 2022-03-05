from apps.places.models import Place
from rest_framework import serializers

__all__ = ["PlaceSerializer"]


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
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
