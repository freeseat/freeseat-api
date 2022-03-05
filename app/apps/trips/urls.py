from apps.trips.api import (
    DriverTripRequestAPIViewSet,
    PassengerTripRequestAPIViewSet,
    TripRequestStartingPointViewSet,
)
from rest_framework import routers

router = routers.DefaultRouter()

app_name = "trips"

router.register(
    r"driver/requested-trips",
    DriverTripRequestAPIViewSet,
    basename="driver-trip-requests",
)
router.register(
    r"driver/passenger-starting-points",
    TripRequestStartingPointViewSet,
    basename="passenger-starting-points",
)
router.register(
    r"passenger/requested-trips",
    PassengerTripRequestAPIViewSet,
    basename="passenger-trip-requests",
)

urlpatterns = router.urls
