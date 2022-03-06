from apps.trips.api import (
    DriverTripRequestAPIViewSet,
    PassengerTripRequestAPIViewSet,
    WaitingPassengerViewSet,
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
    r"driver/waiting-passengers",
    WaitingPassengerViewSet,
    basename="waiting-passengers",
)
router.register(
    r"passenger/requested-trips",
    PassengerTripRequestAPIViewSet,
    basename="passenger-trip-requests",
)

urlpatterns = router.urls
