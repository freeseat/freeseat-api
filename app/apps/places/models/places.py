from django.contrib.gis.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_admin_geomap import GeoItem
from packages.django.db import AbstractUUIDModel

__all__ = ["Place"]


class Place(AbstractUUIDModel, GeoItem):
    created_at = models.DateTimeField(
        verbose_name=_("created at"), auto_now_add=True, editable=False, db_index=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"), auto_now=True, editable=False, db_index=True
    )
    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to="accounts.User",
        on_delete=models.PROTECT,
        related_name="+",
        editable=False,
        db_index=True,
        null=True,
    )

    name = models.CharField(verbose_name=_("name"), max_length=255, db_index=True)
    description = models.TextField(
        verbose_name=_("description"), blank=True, default=""
    )

    is_active = models.BooleanField(
        verbose_name=_("active"), default=True, db_index=True
    )

    point = models.PointField(
        verbose_name=_("point"),
        geography=True,
        spatial_index=True,
    )

    category = models.ForeignKey(
        verbose_name=_("category"),
        to="places.PlaceCategory",
        related_name="places",
        on_delete=models.PROTECT,
        db_index=True,
        null=True,
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("place")
        verbose_name_plural = _("places")

    def __str__(self):
        return self.name

    @property
    def geomap_longitude(self):
        return self.point.x if self.point.x else None

    @property
    def geomap_latitude(self):
        return self.point.y if self.point.y else None

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
        return (
            f"<b><a href={self.admin_url}>{self.name}</a></b>"
            f"<p>{self.description}</p>"
        )

    @property
    def geomap_popup_edit(self):
        return self.geomap_popup_view

    @property
    def geomap_popup_common(self):
        return self.geomap_popup_view
