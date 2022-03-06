from apps.accounts.api import LanguageListAPIView, UserSessionCreateAPIView
from django.urls import path

app_name = "accounts"

urlpatterns = [
    path(
        "user-sessions/", UserSessionCreateAPIView.as_view(), name="user-sessions-list"
    ),
    # TODO: drop
    path("languages/", LanguageListAPIView.as_view(), name="languages-list"),
]
