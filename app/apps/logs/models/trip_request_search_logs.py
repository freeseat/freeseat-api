from django.contrib.gis.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_admin_geomap import GeoItem
from packages.django.db.models import AbstractUUIDModel

__all__ = ["TripRequestSearchLog"]


class TripRequestSearchLog(AbstractUUIDModel, GeoItem):
    user_session = models.ForeignKey(
        verbose_name=_("user session"),
        to="accounts.UserSession",
        related_name="logged_trip_search_requests",
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )

    spoken_languages = models.ManyToManyField(
        verbose_name=_("spoken languages"),
        to="accounts.Language",
        related_name="+",
        null=True,
        blank=True,
    )

    number_of_people = models.PositiveSmallIntegerField(
        verbose_name=_("number of people"),
        default=None,
        null=True,
        db_index=True,
    )

    with_pets = models.BooleanField(
        verbose_name=_("with pets"),
        default=None,
        null=True,
        db_index=True,
    )

    luggage_size = models.IntegerField(
        verbose_name=_("luggage size"),
        default=None,
        null=True,
        db_index=True,
    )

    point = models.PointField(
        verbose_name=_("point"),
        geography=True,
        spatial_index=True,
        null=True,
        blank=True,
    )

    area = models.PolygonField(
        verbose_name=_("area"),
        geography=True,
        spatial_index=True,
        null=True,
        blank=True,
    )

    radius = models.IntegerField(
        verbose_name=_("radius"),
        db_index=True,
        null=True,
        blank=True,
    )

    number_of_results = models.PositiveIntegerField(
        verbose_name=_("number of results"),
        db_index=True,
    )

    results = models.ManyToManyField(
        verbose_name=_("results"),
        to="trips.TripRequest",
        related_name=_("displays"),
    )

    class Meta:
        verbose_name = _("trip request search log")
        verbose_name_plural = _("trip request search logs")
        ordering = ("-created_at",)

    @property
    def geomap_longitude(self):
        return self.point.x if self.point else None

    @property
    def geomap_latitude(self):
        return self.point.y if self.point else None

    @property
    def geomap_icon(self):
        return self.default_icon

    @property
    def admin_url(self):
        return reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=[self.id],
        )

    @property
    def geomap_popup_view(self):
        return f"<b><a href={self.admin_url}>{self.id}</a></b>"

    @property
    def geomap_popup_edit(self):
        return self.geomap_popup_view

    @property
    def geomap_popup_common(self):
        return self.geomap_popup_view
