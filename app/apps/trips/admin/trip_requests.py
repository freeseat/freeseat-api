from apps.trips.models import TripRequest
from django.contrib.gis import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
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
        "link_to_trip",
        "state",
        "is_verified",
        "comment",
        "number_of_displays",
    )
    list_editable = (
        "state",
        "is_verified",
    )
    search_fields = ("comment",)
    list_filter = (
        "is_verified",
        "last_active_at",
        "created_at",
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

    @admin.display(description=_("trip"))
    def link_to_trip(self, obj):
        if obj.trip:
            link = reverse("admin:trips_trip_change", args=[obj.trip_id])
            return format_html('<a href="%s">%s</a>' % (link, obj.trip))

    def number_of_displays(self, obj):
        return obj.number_of_displays

    number_of_displays.admin_order_field = "number_of_displays"

    def get_queryset(self, request):
        # TODO: move to QuerySet
        qs = (
            super().get_queryset(request).annotate(number_of_displays=Count("displays"))
        )
        return qs
