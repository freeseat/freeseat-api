from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from packages.django.db import AbstractUUIDModel


class WayPoint(AbstractUUIDModel):
    trip = models.ForeignKey(
        verbose_name=_("trip"),
        to="trips.Trip",
        on_delete=models.CASCADE,
        related_name="waypoints",
        null=True,
        db_index=True,
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=_("order"),
        db_index=True,
    )

    point = models.PointField(
        verbose_name=_("point"),
        geography=True,
        spatial_index=True,
    )

    class Meta:
        verbose_name = _("waypoint")
        verbose_name_plural = _("waypoints")
        ordering = ("order",)
        unique_together = (
            "order",
            "trip",
        )
