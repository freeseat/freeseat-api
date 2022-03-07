from apps.accounts.models import ContactInformation
from rest_framework import serializers

__all__ = ["ContactInformationSerializer"]


class ContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = [
            "phone_number",
        ]
