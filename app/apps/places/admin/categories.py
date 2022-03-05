from apps.places.models import POICategory
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from packages.django.contrib.admin import CreatedByUserAdminMixin
from simple_history.admin import SimpleHistoryAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

__all__ = ["POICategoryAdmin"]


@admin.register(POICategory)
class POICategoryAdmin(
    TranslationAdmin, SimpleHistoryAdmin, CreatedByUserAdminMixin, TreeAdmin
):
    list_display = ("name", "created_at", "updated_at", "link_to_created_by")
    readonly_fields = (
        "id",
        "path",
        "depth",
        "numchild",
        "created_at",
        "updated_at",
        "created_by",
    )
    form = movenodeform_factory(POICategory)
    search_fields = ("name",)
    list_filter = ("is_active",)
