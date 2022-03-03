from apps.trips.models import WayPoint
from django.contrib.gis import admin
from django.contrib.gis.db.models import PointField
from django.contrib.gis.forms.widgets import OSMWidget

__all__ = []


class WayPointInline(admin.TabularInline):
    model = WayPoint
    min_num = 2
    extra = 0
    formfield_overrides = {
        PointField: {"widget": OSMWidget},
    }
