from apps.places.models import PointOfInterest
from django.contrib.gis import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_admin_geomap import ModelAdmin as GeoMapModelAdmin
from modeltranslation.admin import TranslationAdmin
from packages.django.contrib.admin import CreatedByUserAdminMixin
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["PointOfInterestAdmin"]


@admin.register(PointOfInterest)
class PointOfInterestAdmin(
    CreatedByUserAdminMixin,
    TranslationAdmin,
    SimpleHistoryAdmin,
    GeoMapModelAdmin,
    admin.OSMGeoAdmin,
):
    list_display = (
        "name",
        "link_to_category",
        "link_to_created_by",
        "is_active",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "created_by",
    )
    date_hierarchy = "created_at"
    list_display_links = ("name",)
    autocomplete_fields = ("category",)
    list_filter = ("is_active",)

    geomap_default_longitude = "20"
    geomap_default_latitude = "50.05"
    geomap_default_zoom = "12"
    geomap_height = "750px"

    @admin.display(description=_("category"))
    def link_to_category(self, obj):
        if obj.category_id:
            link = reverse("admin:places_poicategory_change", args=[obj.category_id])
            return format_html('<a href="%s">%s</a>' % (link, obj.category))
