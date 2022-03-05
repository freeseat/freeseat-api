# Generated by Django 4.0.3 on 2022-03-04 22:59

from django.db import migrations, transaction


@transaction.atomic
def create_starting_points_fwd(apps, schema_editor):
    TripRequest = apps.get_model("trips", "TripRequest")

    for trip_request in TripRequest.objects.all():
        if trip_request.trip and (waypoint := trip_request.trip.waypoints.first()):
            trip_request.starting_point = waypoint.point
            trip_request.save(update_fields=["starting_point"])


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0007_historicaltriprequest_starting_point_and_more"),
    ]

    operations = [
        migrations.RunPython(
            create_starting_points_fwd,
            migrations.RunPython.noop,
        )
    ]