from apps.comments.models import Comment
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from packages.django.contrib.admin import (
    ContentObjectAdminMixin,
    CreatedByUserAdminMixin,
)
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["CommentAdmin"]


@admin.register(Comment)
class CommentAdmin(
    CreatedByUserAdminMixin, ContentObjectAdminMixin, SimpleHistoryAdmin
):
    list_display = (
        "content",
        "created_at",
        "link_to_content_object",
    )


class CommentInline(GenericTabularInline):
    model = Comment
    extra = 0
