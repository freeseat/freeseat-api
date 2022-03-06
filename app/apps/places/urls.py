from apps.places.api import POICategoryAPIViewSet, PointOfInterestAPIViewSet
from rest_framework import routers

router = routers.DefaultRouter()

app_name = "places"

router.register(r"poi-categories", POICategoryAPIViewSet, basename="categories")
router.register(
    r"points-of-interest", PointOfInterestAPIViewSet, basename="points-of-interest"
)

urlpatterns = router.urls
