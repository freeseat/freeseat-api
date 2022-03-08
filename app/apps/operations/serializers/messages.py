from apps.operations.models import Message
from rest_framework import serializers

__all__ = ["MessageSerializer"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "full_name",
            "email",
            "phone_number",
            "subject",
            "content",
        ]
