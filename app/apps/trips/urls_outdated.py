from apps.trips.api.trip_requests_outdated import TripRequestOutdatedAPIViewSet
from rest_framework import routers

router = routers.DefaultRouter()

app_name = "trips"

router.register(
    r"requested-trips", TripRequestOutdatedAPIViewSet, basename="trip-requests-outdated"
)

urlpatterns = router.urls
