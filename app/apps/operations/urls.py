from apps.operations.api import MessageCreateAPIView
from django.urls import path

app_name = "operations"

urlpatterns = [
    path("feedback/", MessageCreateAPIView.as_view(), name="message-create"),
]
