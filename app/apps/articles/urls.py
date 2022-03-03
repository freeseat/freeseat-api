from apps.articles.api import ArticlesAPIViewSet
from rest_framework import routers

router = routers.DefaultRouter()

app_name = "trips"

router.register(r"articles", ArticlesAPIViewSet, basename="articles")

urlpatterns = router.urls
