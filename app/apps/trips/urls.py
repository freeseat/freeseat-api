from apps.trips.api import TripRequestAPIViewSet
from rest_framework import routers

router = routers.DefaultRouter()

app_name = "trips"

router.register(r"requested-trips", TripRequestAPIViewSet, basename="trip-requests")

urlpatterns = router.urls
