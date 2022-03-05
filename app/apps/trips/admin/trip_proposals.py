from apps.trips.models import TripProposal
from django.contrib.gis import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_admin_geomap import ModelAdmin as GeoMapModelAdmin
from packages.django.contrib.admin import CreatedByUserAdminMixin
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["TripProposalAdmin"]


@admin.register(TripProposal)
class TripProposalAdmin(
    CreatedByUserAdminMixin, SimpleHistoryAdmin, GeoMapModelAdmin, admin.OSMGeoAdmin
):
    list_display = (
        "id",
        "departure_time",
        "number_of_seats",
        "pets_allowed",
        "luggage_carrier_size",
        "link_to_trip",
        "state",
        "comment",
    )
    list_editable = ("state",)
    search_fields = ("comment",)
    list_filter = (
        "spoken_languages",
        "pets_allowed",
        "luggage_carrier_size",
        "state",
    )
    filter_horizontal = ("spoken_languages",)
    readonly_fields = (
        "id",
        "created_by",
        "user_session",
    )
    raw_id_fields = (
        "trip",
        "contact_information",
    )
    date_hierarchy = "departure_time"

    geomap_default_longitude = "20"
    geomap_default_latitude = "50.05"
    geomap_default_zoom = "6"
    geomap_height = "750px"

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ("state",)
        return super().get_readonly_fields(request, obj)

    @admin.display(description=_("trip"))
    def link_to_trip(self, obj):
        if obj.trip:
            link = reverse("admin:trips_trip_change", args=[obj.trip_id])
            return format_html('<a href="%s">%s</a>' % (link, obj.trip))
