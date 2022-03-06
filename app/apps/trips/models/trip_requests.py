from django.contrib.gis.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_admin_geomap import GeoItem
from packages.django.db.models import AbstractUUIDModel

__all__ = ["TripRequest"]


class TripRequestManager(models.Manager):
    def active(self):
        now = timezone.now()
        past_24_hours = now - timezone.timedelta(hours=24)

        return self.model.objects.filter(
            state=self.model.TripRequestState.ACTIVE,
            last_active_at__gte=past_24_hours,
        )


class TripRequest(AbstractUUIDModel, GeoItem):
    objects = TripRequestManager()

    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to="accounts.User",
        related_name="created_trip_requests",
        on_delete=models.CASCADE,
        db_index=True,
        editable=False,
        null=True,
        blank=True,
    )

    user_session = models.ForeignKey(
        verbose_name=_("user session"),
        to="accounts.UserSession",
        related_name="created_trip_requests",
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        blank=True,
        editable=False,
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

    last_active_at = models.DateTimeField(
        verbose_name=_("last active at"),
        auto_now=True,
        editable=False,
        db_index=True,
    )

    spoken_languages = models.ManyToManyField(
        verbose_name=_("spoken languages"),
        to="accounts.Language",
        related_name="+",
    )

    class TripRequestState(models.TextChoices):
        ACTIVE = "active", _("active")
        CANCELLED = "cancelled", _("cancelled")
        COMPLETED = "completed", _("completed")
        OUTDATED = "outdated", _("outdated")
        INVALID = "invalid", _("invalid")

    state = models.CharField(
        max_length=32,
        verbose_name=_("state"),
        default=TripRequestState.ACTIVE,
        choices=TripRequestState.choices,
        db_index=True,
    )

    is_verified = models.BooleanField(
        verbose_name=_("is verified"),
        default=False,
        db_index=True,
    )

    starting_point = models.PointField(
        verbose_name=_("point"),
        geography=True,
        spatial_index=True,
        null=True,
        blank=True,
    )

    number_of_people = models.PositiveSmallIntegerField(
        verbose_name=_("number of people"),
        default=1,
        db_index=True,
    )

    with_pets = models.BooleanField(
        verbose_name=_("with pets"),
        default=False,
        db_index=True,
    )

    class LuggageSize(models.IntegerChoices):
        SMALL_BAGS = 1, _("small bags")
        LARGE_BAGS = 2, _("large bags")
        CARGO = 3, _("cargo")

    luggage_size = models.PositiveSmallIntegerField(
        verbose_name=_("luggage size"),
        default=LuggageSize.SMALL_BAGS,
        choices=LuggageSize.choices,
        db_index=True,
    )

    comment = models.TextField(
        verbose_name=_("comment"),
    )

    allow_partial_trip = models.BooleanField(
        verbose_name=_("allow partial trip"),
        default=False,
        db_index=True,
    )

    trip = models.OneToOneField(
        verbose_name=_("trip"),
        to="trips.Trip",
        on_delete=models.CASCADE,
        related_name="trip_request",
        null=True,
        db_index=True,
    )

    starting_point = models.PointField(
        verbose_name=_("point"),
        geography=True,
        spatial_index=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("trip request")
        verbose_name_plural = _("trip requests")
        ordering = ("-trip__route_length", "-created_at")

    @property
    def geomap_longitude(self):
        return self.starting_point.x if self.starting_point else None

    @property
    def geomap_latitude(self):
        return self.starting_point.y if self.starting_point else None

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
        return f"<b><a href={self.admin_url}>{self.comment}</a></b>"

    @property
    def geomap_popup_edit(self):
        return self.geomap_popup_view

    @property
    def geomap_popup_common(self):
        return self.geomap_popup_view
