from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _
from packages.django.db.models import AbstractUUIDModel

__all__ = ["Ticket"]


class Ticket(AbstractUUIDModel):
    class TicketStatus(models.TextChoices):
        PENDING = "pending", _("pending")
        UNDERWAY = "processing", _("processing")
        PROCESSED = "resolved", _("resolved")
        CANCELLED = "cancelled", _("cancelled")

    class TicketType(models.TextChoices):
        QUESTION = "question", _("question")
        BUG = "bug", _("bug")
        COMPLAINT = "complaint", _("complaint")
        ERROR = "error", _("error")

    class TicketPriority(models.TextChoices):
        LOW = "low", _("low")
        STANDARD = "standard", _("standard")
        HIGH = "high", _("high")
        CRITICAL = "critical", _("critical")

    title = models.CharField(verbose_name=_("title"), max_length=255, db_index=True)
    content = models.TextField(verbose_name=_("content"))
    type = models.CharField(
        verbose_name=_("type"),
        choices=TicketType.choices,
        default=TicketType.QUESTION,
        max_length=64,
        db_index=True,
    )
    status = models.CharField(
        verbose_name=_("status"),
        choices=TicketStatus.choices,
        default=TicketStatus.PENDING,
        max_length=64,
        db_index=True,
    )
    priority = models.CharField(
        verbose_name=_("priority"),
        choices=TicketPriority.choices,
        default=TicketPriority.STANDARD,
        max_length=64,
        db_index=True,
    )
    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to="accounts.User",
        related_name="opened_tickets",
        on_delete=models.PROTECT,
        editable=False,
        null=True,
        db_index=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"), auto_now_add=True, editable=False, db_index=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"), auto_now=True, editable=False, db_index=True
    )
    manager = models.ForeignKey(
        verbose_name=_("current manager"),
        to="accounts.User",
        related_name="tickets",
        on_delete=models.PROTECT,
        limit_choices_to={"is_staff": True},
        null=True,
        blank=True,
    )

    content_type = models.ForeignKey(
        verbose_name=_("content type"),
        to="contenttypes.ContentType",
        on_delete=models.PROTECT,
        db_index=True,
    )
    object_id = models.UUIDField(verbose_name=_("object id"))
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _("ticket")
        verbose_name_plural = _("tickets")
        ordering = ("-created_at",)

    def __str__(self):
        return self.title
