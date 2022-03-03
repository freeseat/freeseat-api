from apps.trips.api import TripRequestsAPIViewSet
from rest_framework import routers

router = routers.DefaultRouter()

app_name = "trips"

router.register(r"requested-trips", TripRequestsAPIViewSet, basename="requested-trips")

urlpatterns = router.urls
