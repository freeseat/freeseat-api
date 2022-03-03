from django.db import models
from django.utils.translation import gettext_lazy as _
from packages.django.db.models import AbstractUUIDModel

__all__ = ["Article"]


class Article(AbstractUUIDModel):
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"),
        auto_now=True,
        editable=False,
        db_index=True,
    )
    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to="accounts.User",
        on_delete=models.PROTECT,
        editable=False,
        db_index=True,
    )
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
        db_index=True,
    )

    content = models.TextField()

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")
        ordering = ("-created_at",)

    def __str__(self):
        return self.name
