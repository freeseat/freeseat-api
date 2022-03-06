from apps.operations.api import LanguageListAPIView
from django.urls import path

app_name = "operations"

urlpatterns = [
    path("languages/", LanguageListAPIView.as_view(), name="languages-list"),
]
