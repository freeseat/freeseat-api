from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ["Country"]


class Country(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"), auto_now=True, editable=False, db_index=True
    )
    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to="accounts.User",
        related_name="+",
        on_delete=models.SET_NULL,
        db_index=True,
        editable=False,
        null=True,
        blank=True,
    )
    code = models.CharField(
        verbose_name=_("code"),
        max_length=2,
        db_index=True,
    )
    name = models.CharField(verbose_name=_("name"), max_length=255, db_index=True)
    territory = models.MultiPolygonField(
        verbose_name=_("territory"), geography=True, spatial_index=True
    )

    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")
        ordering = ("code",)

    def __str__(self):
        return self.code
