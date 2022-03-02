# Generated by Django 4.0.1 on 2022-03-02 20:45

import uuid

import django.contrib.gis.db.models.fields
import django.db.models.deletion
import django_admin_geomap
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0002_usersession_language_historicallanguage"),
    ]

    operations = [
        migrations.CreateModel(
            name="TripRequest",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="id",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="created at"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="updated at"
                    ),
                ),
                (
                    "last_active_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="last ative at"
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("active", "active"),
                            ("cancelled", "cancelled"),
                            ("completed", "completed"),
                            ("outdated", "outdated"),
                        ],
                        db_index=True,
                        default="active",
                        max_length=32,
                        verbose_name="state",
                    ),
                ),
                (
                    "number_of_people",
                    models.PositiveSmallIntegerField(
                        db_index=True, default=1, verbose_name="number of people"
                    ),
                ),
                (
                    "with_pets",
                    models.BooleanField(
                        db_index=True, default=False, verbose_name="with pets"
                    ),
                ),
                (
                    "luggage_size",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "small bags"), (2, "large bags"), (3, "cargo")],
                        db_index=True,
                        default=1,
                        verbose_name="luggage size",
                    ),
                ),
                ("comment", models.TextField(verbose_name="comment")),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_trip_requests",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
                (
                    "spoken_languages",
                    models.ManyToManyField(
                        related_name="+",
                        to="accounts.Language",
                        verbose_name="spoken languages",
                    ),
                ),
                (
                    "user_session",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_trip_requests",
                        to="accounts.usersession",
                        verbose_name="user session",
                    ),
                ),
            ],
            options={
                "verbose_name": "trip",
                "verbose_name_plural": "trips",
                "ordering": ("created_at",),
            },
            bases=(models.Model, django_admin_geomap.GeoItem),
        ),
        migrations.CreateModel(
            name="HistoricalTripRequest",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        verbose_name="id",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        editable=False,
                        verbose_name="created at",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        editable=False,
                        verbose_name="updated at",
                    ),
                ),
                (
                    "last_active_at",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        editable=False,
                        verbose_name="last ative at",
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("active", "active"),
                            ("cancelled", "cancelled"),
                            ("completed", "completed"),
                            ("outdated", "outdated"),
                        ],
                        db_index=True,
                        default="active",
                        max_length=32,
                        verbose_name="state",
                    ),
                ),
                (
                    "number_of_people",
                    models.PositiveSmallIntegerField(
                        db_index=True, default=1, verbose_name="number of people"
                    ),
                ),
                (
                    "with_pets",
                    models.BooleanField(
                        db_index=True, default=False, verbose_name="with pets"
                    ),
                ),
                (
                    "luggage_size",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "small bags"), (2, "large bags"), (3, "cargo")],
                        db_index=True,
                        default=1,
                        verbose_name="luggage size",
                    ),
                ),
                ("comment", models.TextField(verbose_name="comment")),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField()),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_session",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="accounts.usersession",
                        verbose_name="user session",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical trip",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="WayPoint",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="id",
                    ),
                ),
                (
                    "order",
                    models.PositiveSmallIntegerField(
                        db_index=True, verbose_name="order"
                    ),
                ),
                (
                    "point",
                    django.contrib.gis.db.models.fields.PointField(
                        geography=True, srid=4326, verbose_name="point"
                    ),
                ),
                (
                    "trip_request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="waypoints",
                        to="trips.triprequest",
                        verbose_name="trip request",
                    ),
                ),
            ],
            options={
                "verbose_name": "waypoint",
                "verbose_name_plural": "waypoints",
                "ordering": ("order",),
                "unique_together": {("order", "trip_request")},
            },
        ),
    ]
