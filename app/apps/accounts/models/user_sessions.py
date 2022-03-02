from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ["UserSession"]


class UserSession(models.Model):
    id = models.CharField(
        verbose_name=_("id"),
        max_length=255,
        primary_key=True,
        editable=False,
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )
    user = models.ForeignKey(
        verbose_name=_("user"),
        to="accounts.User",
        related_name="user_sessions",
        on_delete=models.CASCADE,
        db_index=True,
        editable=False,
        null=True,
    )
    cookies_accepted_at = models.DateTimeField(
        verbose_name=_("cookies accepted at"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )

    class Meta:
        verbose_name = _("user session")
        verbose_name_plural = _("user sessions")
        ordering = ("id",)
