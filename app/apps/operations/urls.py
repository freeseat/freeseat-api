from apps.operations.api import MessageCreateAPIView, StatusRetrieveAPIView
from django.urls import path

app_name = "operations"

urlpatterns = [
    path("feedback/", MessageCreateAPIView.as_view(), name="message-create"),
    path("status/", StatusRetrieveAPIView.as_view(), name="status-retrieve"),
]
