from apps.accounts.models import UserSession
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["UserSessionAdmin"]


@admin.register(UserSession)
class UserSessionAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "created_at",
        "last_active_at",
    )
    readonly_fields = (
        "id",
        "created_at",
        "last_active_at",
    )
    date_hierarchy = "created_at"
    list_filter = ("last_active_at", "created_at")

    def has_add_permission(self, request):
        return False
