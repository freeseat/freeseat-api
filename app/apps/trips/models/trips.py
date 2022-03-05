from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from packages.django.db import AbstractUUIDModel

__all__ = ["Trip"]


class Trip(AbstractUUIDModel):
    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to="accounts.User",
        related_name="created_trips",
        on_delete=models.CASCADE,
        db_index=True,
        editable=False,
        null=True,
        blank=True,
    )

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

    route = models.LineStringField(
        verbose_name=_("route"),
        null=True,
        blank=True,
        spatial_index=True,
        geography=True,
    )

    route_length = models.FloatField(
        verbose_name=_("route length"), null=True, db_index=True
    )

    class Meta:
        verbose_name = _("trip")
        verbose_name_plural = _("trips")
        ordering = ("-created_at",)
