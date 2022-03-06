from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _
from packages.django.db.models import AbstractUUIDModel

__all__ = ["Comment"]


class Comment(AbstractUUIDModel):
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"), auto_now=True, editable=False, db_index=True
    )

    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_comments",
        editable=False,
        null=True,
        db_index=True,
    )

    content = models.TextField(verbose_name=_("content"))

    content_type = models.ForeignKey(
        verbose_name=_("content type"),
        to="contenttypes.ContentType",
        on_delete=models.PROTECT,
        db_index=True,
    )
    object_id = models.UUIDField(verbose_name=_("object id"), db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")

    comments = GenericRelation(
        verbose_name=_("comments"),
        to="comments.Comment",
        related_name="%(class)",
    )

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        ordering = ("-created_at",)

    def __str__(self):
        return self.content
