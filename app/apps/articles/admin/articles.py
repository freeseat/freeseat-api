from apps.articles.models import Article
from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from packages.django.contrib.admin import CreatedByUserAdminMixin
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["ArticleAdmin"]


@admin.register(Article)
class ArticleAdmin(CreatedByUserAdminMixin, TabbedTranslationAdmin, SimpleHistoryAdmin):
    list_display = (
        "name",
        "link_to_created_by",
        "created_at",
    )
    search_fields = (
        "name",
        "content",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "created_by",
        "created_at",
        "updated_at",
    )

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ()
        return super().get_readonly_fields(request, obj)
