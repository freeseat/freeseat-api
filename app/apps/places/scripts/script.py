import json
from apps.places.models import PointOfInterest
from django.contrib.gis.geos import GEOSGeometry


def import_script():
    with open("coords.json") as file:
        data = json.load(file)


        for feature in data:
            name = feature.get("name")
            description = feature.get("description")
            url = feature.get("resource_url")
            point = feature.get("point")

            PointOfInterest.objects.create(
                category_id="city",
                name=name,
                description=description,
                url=url,
                point=GEOSGeometry(str(point)),
            )
