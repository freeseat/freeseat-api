from apps.trips.api import TripRequestAPIViewSet, TripRequestStartingPointViewSet
from rest_framework import routers

router = routers.DefaultRouter()

app_name = "trips"

router.register(r"requested-trips", TripRequestAPIViewSet, basename="trip-requests")
router.register(
    r"passengers/starting-points",
    TripRequestStartingPointViewSet,
    basename="passenger-starting-points",
)

urlpatterns = router.urls
