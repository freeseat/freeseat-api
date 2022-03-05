from apps.accounts.models import ContactInformation
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["ContactInformationAdmin"]


@admin.register(ContactInformation)
class ContactInformationAdmin(SimpleHistoryAdmin):
    list_display = ("first_name", "last_name", "phone_number", "email")
