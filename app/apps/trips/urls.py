from apps.trips.api import TripRequestAPIViewSet, TripRequestStartingPointViewSet
from rest_framework import routers

router = routers.DefaultRouter()

app_name = "trips"

router.register(r"driver/requested-trips", TripRequestAPIViewSet, basename="driver-trip-requests")
router.register(r"passenger/requested-trips", TripRequestAPIViewSet, basename="passenger-trip-requests")
router.register(
    r"passenger/starting-points",
    TripRequestStartingPointViewSet,
    basename="passenger-starting-points",
)

urlpatterns = router.urls
