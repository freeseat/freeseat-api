from apps.places.api import PlaceAPIViewSet, PlaceCategoryAPIViewSet
from rest_framework import routers

router = routers.DefaultRouter()

app_name = "places"

router.register(r"places", PlaceAPIViewSet, basename="places")
router.register(r"categories", PlaceCategoryAPIViewSet, basename="categories")

urlpatterns = router.urls
