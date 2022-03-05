from apps.trips.enums import LuggageSize, TripState
from django.contrib.gis.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_admin_geomap import GeoItem
from packages.django.db.models import AbstractUUIDModel

__all__ = ["TripProposal"]


class TripProposalManager(models.Manager):
    def active(self):
        return self.model.objects.filter(
            state=TripState.ACTIVE,
            departure_time__gte=timezone.now(),
        )


class TripProposal(AbstractUUIDModel, GeoItem):
    objects = TripProposalManager()

    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to="accounts.User",
        related_name="created_trip_proposals",
        on_delete=models.CASCADE,
        db_index=True,
        editable=False,
        null=True,
        blank=True,
    )

    user_session = models.ForeignKey(
        verbose_name=_("user session"),
        to="accounts.UserSession",
        related_name="created_trip_proposals",
        on_delete=models.CASCADE,
        db_index=True,
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

    departure_time = models.DateTimeField(
        verbose_name=_("start time"),
        db_index=True,
    )

    spoken_languages = models.ManyToManyField(
        verbose_name=_("spoken languages"),
        to="accounts.Language",
        related_name="+",
    )

    state = models.CharField(
        max_length=32,
        verbose_name=_("state"),
        default=TripState.ACTIVE,
        choices=TripState.choices,
        db_index=True,
    )

    number_of_seats = models.PositiveSmallIntegerField(
        verbose_name=_("number of seats"),
        default=4,
        db_index=True,
    )

    pets_allowed = models.BooleanField(
        verbose_name=_("pets allowed"),
        default=False,
        db_index=True,
    )

    luggage_carrier_size = models.PositiveSmallIntegerField(
        verbose_name=_("luggage carrier size"),
        default=LuggageSize.SMALL_BAGS,
        choices=LuggageSize.choices,
        db_index=True,
    )

    comment = models.TextField(
        verbose_name=_("comment"),
    )

    contact_information = models.OneToOneField(
        verbose_name=_("contact information"),
        to="accounts.ContactInformation",
        related_name="+",
        on_delete=models.CASCADE,
    )

    trip = models.OneToOneField(
        verbose_name=_("trip"),
        to="trips.Trip",
        on_delete=models.CASCADE,
        related_name="trip_proposal",
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
        verbose_name = _("trip proposal")
        verbose_name_plural = _("trip proposals")
        ordering = ("departure_time",)

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
