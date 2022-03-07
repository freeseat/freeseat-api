from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from apps.places.models import Country
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

    country = models.ForeignKey(
        verbose_name=_("country"),
        to="places.Country",
        on_delete=models.SET_NULL,
        related_name=_("waypoints"),
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        verbose_name = _("waypoint")
        verbose_name_plural = _("waypoints")
        ordering = ("order",)
        unique_together = (
            "order",
            "trip",
        )

    @classmethod
    def update_country_based_on_location(cls, sender, instance, *args, **kwargs):
        print('updating')
        country = Country.objects.filter(
            territory__covers=instance.point
        ).first()
        instance.country = country
        print(country)


pre_save.connect(WayPoint.update_country_based_on_location, sender=WayPoint)
