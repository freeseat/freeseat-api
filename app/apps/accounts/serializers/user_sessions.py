from apps.accounts.models import UserSession
from rest_framework import serializers

__all__ = ["UserSessionSerializer"]


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = [
            "id",
        ]
