from apps.operations.models import Ticket
from django.contrib import admin
from packages.django.contrib.admin import CreatedByUserAdminMixin
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["TicketAdmin"]


@admin.register(Ticket)
class TicketAdmin(CreatedByUserAdminMixin, SimpleHistoryAdmin):
    list_display = (
        "title",
        "created_at",
    )
