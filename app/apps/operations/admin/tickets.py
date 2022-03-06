from apps.comments.admin.comments import CommentInline
from apps.operations.models import Ticket
from django.contrib import admin
from packages.django.contrib.admin import (
    ContentObjectAdminMixin,
    CreatedByUserAdminMixin,
)
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["TicketAdmin"]


@admin.register(Ticket)
class TicketAdmin(CreatedByUserAdminMixin, ContentObjectAdminMixin, SimpleHistoryAdmin):
    list_display = (
        "title",
        "created_at",
        "link_to_content_object",
    )
    inlines = [CommentInline]
