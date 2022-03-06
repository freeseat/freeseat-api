from rest_framework import serializers

__all__ = ["UserSessionSerializer"]


class UserSessionSerializer(serializers.Serializer):
    id = serializers.CharField()
