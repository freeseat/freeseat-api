from apps.operations.models import Message
from django.contrib import admin
from packages.django.contrib.admin import CreatedByUserAdminMixin

__all__ = ["MessageAdmin"]


@admin.register(Message)
class MessageAdmin(CreatedByUserAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "phone_number",
        "subject",
        "was_read",
        "created_at",
    )
    date_hierarchy = "created_at"
    list_filter = ("was_read",)
    list_editable = ("was_read",)
