from apps.accounts.models import ContactInformation
from rest_framework import serializers

__all__ = ["ContactInformationSerializer"]


class ContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
        ]
