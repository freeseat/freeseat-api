from django.db import models
from django.utils.translation import gettext_lazy as _
from packages.django.db.fields import PhoneNumberField
from packages.django.db.models import AbstractUUIDModel

__all__ = ["Message"]


class Message(AbstractUUIDModel):
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )
    email = models.EmailField(
        verbose_name=_("email"), default="", blank=True, db_index=True
    )
    phone_number = PhoneNumberField(
        verbose_name=_("phone number"), default="", null=True, blank=True, db_index=True
    )
    full_name = models.CharField(
        verbose_name=_("full name"),
        max_length=64,
        default="",
        blank=True,
        db_index=True,
    )
    subject = models.CharField(
        verbose_name=_("subject"), max_length=255, default="", blank=True, db_index=True
    )
    content = models.TextField(verbose_name=_("content"))
    was_read = models.BooleanField(
        verbose_name=_("was read"), default=False, db_index=True
    )

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")
        ordering = ("-created_at",)
