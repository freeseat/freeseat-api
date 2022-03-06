from apps.accounts.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["UserAdmin"]


@admin.register(User)
class UserAdmin(SimpleHistoryAdmin, UserAdmin):
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
    exclude = ("user_permissions",)
    list_horizontal = ("groups",)
    fieldsets = ()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.registration_source = User.RegistrationSource.ADMIN_PANEL
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ()
        return super().get_readonly_fields(request, obj)

    def get_exclude(self, request, obj=None):
        if not request.user.is_superuser:
            return ("is_superuser",) + self.exclude
        return super().get_exclude(request, obj)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True

        if request.user.is_superuser:
            return True

        if obj == request.user:
            return True

        if request.user.is_staff and not obj.is_superuser:
            return True

        return False
