from apps.trips.admin.waypoints import WayPointInline
from apps.trips.models import Trip
from django.contrib.gis import admin
from packages.django.contrib.admin import CreatedByUserAdminMixin
from simple_history.admin import SimpleHistoryAdmin

__all__ = []


@admin.register(Trip)
class TripAdmin(CreatedByUserAdminMixin, SimpleHistoryAdmin, admin.GeoModelAdmin):
    list_display = ("id",)
    inlines = [WayPointInline]
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "created_by",
    )
