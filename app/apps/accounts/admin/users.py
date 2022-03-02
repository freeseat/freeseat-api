from apps.accounts.models import User
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["UserAdmin"]


@admin.register(User)
class UserAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "username",
        "phone_number",
        "email",
        "first_name",
        "last_name",
    )
    list_filter = ("is_staff", "is_superuser", "registration_source")
    readonly_fields = ("id", "date_joined", "last_login", "registration_source")
    date_hierarchy = "date_joined"
    filter_horizontal = ("groups", "user_permissions")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.registration_source = User.RegistrationSource.ADMIN_PANEL
        super().save_model(request, obj, form, change)
