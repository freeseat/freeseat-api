# Generated by Django 4.0.3 on 2022-03-06 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0015_tripproposal_historicaltripproposal"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tripproposal",
            options={
                "ordering": ("departure_time",),
                "verbose_name": "trip proposal",
                "verbose_name_plural": "trip proposals",
            },
        ),
        migrations.DeleteModel(
            name="TripRequestSearchLog",
        ),
    ]
