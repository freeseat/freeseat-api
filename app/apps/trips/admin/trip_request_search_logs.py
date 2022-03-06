from apps.trips.models import TripRequestSearchLog
from django.contrib.gis import admin
from django_admin_geomap import ModelAdmin as GeoMapModelAdmin
from packages.django.contrib.admin import CreatedByUserAdminMixin
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["TripRequestSearchLogAdmin"]


@admin.register(TripRequestSearchLog)
class TripRequestSearchLogAdmin(
    CreatedByUserAdminMixin, SimpleHistoryAdmin, GeoMapModelAdmin, admin.OSMGeoAdmin
):
    list_display = (
        "id",
        "created_at",
        "number_of_people",
        "with_pets",
        "luggage_size",
        "radius",
        "number_of_results",
    )
    list_filter = (
        "created_at",
        "with_pets",
        "luggage_size",
        "number_of_people",
    )
    filter_horizontal = (
        "spoken_languages",
        "results",
    )
    date_hierarchy = "created_at"

    geomap_default_longitude = "20"
    geomap_default_latitude = "50.05"
    geomap_default_zoom = "6"
    geomap_height = "750px"

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ("state",)
        return super().get_readonly_fields(request, obj)

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False
