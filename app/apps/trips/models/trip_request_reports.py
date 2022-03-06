from django.db import models
from django.utils.translation import gettext_lazy as _
from packages.django.db.models import AbstractUUIDModel

__all__ = ["TripRequestReport"]


class TripRequestReport(AbstractUUIDModel):
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )

    trip_request = models.OneToOneField(
        verbose_name=_("trip request"),
        to="trips.TripRequest",
        related_name="report",
        on_delete=models.CASCADE,
    )

    class TripRequestResult(models.TextChoices):
        TRANSPORT_WAS_NOT_FOUND = "was_not_found", _("transport was not found")
        TRANSPORT_NOT_REQUIRED = "not_required", _("transport not required")
        TRANSPORT_WAS_FOUND_ON_PLATFORM = "found_on_platform", _(
            "transport was found on platform"
        )
        TRANSPORT_WAS_FOUND_IN_OTHER_PLACE = "found_in_other_place", _(
            "transport was found in other place"
        )

    result = models.CharField(
        verbose_name=_("result"),
        max_length=32,
        choices=TripRequestResult.choices,
        default="",
        db_index=True,
        blank=True,
    )

    class SatisfactionRate(models.IntegerChoices):
        DISAPPOINTED = 0, _("disappointed")
        NOT_SATISFIED = 1, _("not satisfied")
        RATHER_SATISFIED = 3, _("rather satisfied")
        SATISFIED = 4, _("satisfied")
        ADMIRED = 5, _("admired")

    satisfaction_rate = models.PositiveSmallIntegerField(
        verbose_name=_("satisfaction rate"),
        choices=SatisfactionRate.choices,
        db_index=True,
        null=True,
    )

    class Meta:
        verbose_name = _("trip request report")
        verbose_name_plural = _("trip request reports")
        ordering = ("-created_at",)
