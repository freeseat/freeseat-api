# Generated by Django 4.0.3 on 2022-03-04 21:03

from django.db import migrations, transaction


@transaction.atomic
def create_trips_for_trip_requests_fwd(apps, schema_editor):
    TripRequest = apps.get_model("trips", "TripRequest")
    Trip = apps.get_model("trips", "Trip")
    Waypoint = apps.get_model("trips", "Waypoint")

    for trip_request in TripRequest.objects.all():
        if not trip_request.trip:
            trip = Trip.objects.create(
                created_at=trip_request.created_at,
                created_by=trip_request.created_by,
                route_length=trip_request.route_length,
            )
            trip_request.trip = trip
            trip_request.save(update_fields=["trip"])

    for waypoint in Waypoint.objects.all():
        if waypoint.trip_request:
            waypoint.trip = waypoint.trip_request.trip
            waypoint.trip_request = None
            waypoint.save(update_fields=["trip", "trip_request"])


@transaction.atomic
def create_trips_for_trip_requests_bwd(apps, schema_editor):
    TripRequest = apps.get_model("trips", "TripRequest")

    for trip_request in TripRequest.objects.all():
        if trip := trip_request.trip:
            trip_request.route_length = trip.route_length
            trip_request.trip = None
            trip_request.save(update_fields=["trip", "route_length"])

            for waypoint in trip.waypoints.all():
                waypoint.trip_request = trip_request
                waypoint.trip = None
                waypoint.save(update_fields=["trip", "trip_request"])

            trip.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0005_alter_historicaltriprequest_options_and_more"),
    ]

    operations = [
        migrations.RunPython(
            create_trips_for_trip_requests_fwd,
            create_trips_for_trip_requests_bwd,
        )
    ]
