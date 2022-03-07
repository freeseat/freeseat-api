import json

from apps.places.models import Country
from django.contrib.gis import geos


def import_script():
    with open("../../../../data/countries.geojson") as file:
        gj = json.load(file)
        features = gj["features"]

        i = 0
        for feature in features:
            geometry = feature.get("geometry")

            if geometry.get("type") == "Polygon":
                geometry["type"] = "MultiPolygon"
                geometry["coordinates"] = [geometry.get("coordinates")]
            geom = geos.GEOSGeometry(str(feature["geometry"]))

            properties = feature.get("properties")
            name = properties.get("ADMIN")
            code = properties.get("ISO_A3")

            try:
                Country.objects.create(
                    name=name,
                    code=code,
                    territory=geom,
                )
            except Exception as e:
                print(e)

            i += 1
            print(f"country created: {code}")

        print(f"{i} countries created")
