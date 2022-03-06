from apps.trips.models import TripRequestReport
from django.contrib import admin


@admin.register(TripRequestReport)
class TripRequestReportAdmin(admin.ModelAdmin):
    pass
