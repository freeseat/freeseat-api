from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from packages.django.db import AbstractUUIDModel


class WayPoint(AbstractUUIDModel):
    trip_request = models.ForeignKey(
        verbose_name=_("trip request"),
        to="trips.TripRequest",
        on_delete=models.CASCADE,
        related_name="waypoints",
        db_index=True,
    )
    order = models.PositiveSmallIntegerField(
        verbose_name=_("order"),
        db_index=True,
    )
    point = models.PointField(
        verbose_name=_("to point"),
        geography=True,
    )

    class Meta:
        verbose_name = _("waypoint")
        verbose_name_plural = _("waypoints")
        ordering = ("order",)
        unique_together = (
            "order",
            "trip_request",
        )
