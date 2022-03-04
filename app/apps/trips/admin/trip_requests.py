from apps.trips.models import TripRequest
from django.contrib.gis import admin
from django_admin_geomap import ModelAdmin as GeoMapModelAdmin
from packages.django.contrib.admin import CreatedByUserAdminMixin
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["TripRequestAdmin"]


@admin.register(TripRequest)
class TripRequestAdmin(
    CreatedByUserAdminMixin, SimpleHistoryAdmin, GeoMapModelAdmin, admin.OSMGeoAdmin
):
    list_display = (
        "id",
        "created_at",
        "last_active_at",
        "number_of_people",
        "with_pets",
        "luggage_size",
        "allow_partial_trip",
        "state",
        "comment",
    )
    list_editable = ("state",)
    search_fields = ("comment",)
    list_filter = (
        "spoken_languages",
        "with_pets",
        "luggage_size",
        "state",
        "allow_partial_trip",
    )
    filter_horizontal = ("spoken_languages",)
    readonly_fields = (
        "id",
        "created_by",
        "user_session",
    )
    raw_id_fields = ("trip",)
    inlines = []
    date_hierarchy = "last_active_at"
    geomap_default_longitude = "20"
    geomap_default_latitude = "50.05"
    geomap_default_zoom = "6"
    geomap_height = "750px"

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ("state",)
        return super().get_readonly_fields(request, obj)
