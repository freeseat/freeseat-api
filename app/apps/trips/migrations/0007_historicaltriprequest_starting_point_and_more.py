# Generated by Django 4.0.3 on 2022-03-04 22:58

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0006_auto_20220304_2138"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicaltriprequest",
            name="starting_point",
            field=django.contrib.gis.db.models.fields.PointField(
                blank=True, geography=True, null=True, srid=4326, verbose_name="point"
            ),
        ),
        migrations.AddField(
            model_name="triprequest",
            name="starting_point",
            field=django.contrib.gis.db.models.fields.PointField(
                blank=True, geography=True, null=True, srid=4326, verbose_name="point"
            ),
        ),
    ]