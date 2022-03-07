from apps.places.models import Country
from django.contrib.gis import admin
from modeltranslation.admin import TranslationAdmin
from packages.django.contrib.admin import CreatedByUserAdminMixin
from simple_history.admin import SimpleHistoryAdmin

__all__ = ["CountryAdmin"]


@admin.register(Country)
class CountryAdmin(
    CreatedByUserAdminMixin,
    TranslationAdmin,
    SimpleHistoryAdmin,
    admin.OSMGeoAdmin,
):
    list_display = (
        "code",
        "name",
        "link_to_created_by",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
    )
    date_hierarchy = "created_at"
    list_display_links = (
        "code",
        "name",
    )
