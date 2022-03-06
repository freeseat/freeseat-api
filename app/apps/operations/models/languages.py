from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ["Language"]


class Language(models.Model):
    code = models.CharField(
        max_length=4,
        verbose_name=_("code"),
        primary_key=True,
        unique=True,
    )
    name = models.CharField(
        verbose_name=_("name"),
        max_length=128,
        db_index=True,
    )
    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to="accounts.User",
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        db_index=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")
        ordering = ("code",)

    def __str__(self):
        return self.name
