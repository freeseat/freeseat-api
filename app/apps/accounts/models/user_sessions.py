from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ["UserSession"]


class UserSession(models.Model):
    id = models.CharField(
        verbose_name=_("id"),
        max_length=255,
        primary_key=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )
    cookies_accepted_at = models.DateTimeField(
        verbose_name=_("cookies accepted at"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )
    terms_accepted_at = models.DateTimeField(
        verbose_name=_("terms and conditions accepted at"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )
    last_active_at = models.DateTimeField(
        verbose_name=_("last active at"),
        auto_now=True,
        editable=False,
        db_index=True,
    )

    class Meta:
        verbose_name = _("user session")
        verbose_name_plural = _("user sessions")
        ordering = ("id",)
