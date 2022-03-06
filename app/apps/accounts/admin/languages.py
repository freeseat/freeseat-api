# TODO: drop file
from apps.accounts.models import Language
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from packages.django.contrib.admin import CreatedByUserAdminMixin
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["LanguageAdmin"]


@admin.register(Language)
class LanguageAdmin(CreatedByUserAdminMixin, SimpleHistoryAdmin, TranslationAdmin):
    list_display = (
        "code",
        "name",
    )
    readonly_fields = ("code",)
    date_hierarchy = "created_at"
    search_fields = ("code", "name")

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ()
        return super().get_readonly_fields(request, obj)
