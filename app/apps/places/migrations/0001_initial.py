# Generated by Django 4.0.3 on 2022-03-05 00:29

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
    ]

    operations = [
        migrations.CreateModel(
            name="PlaceCategory",
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
                ("path", models.CharField(max_length=255, unique=True)),
                ("depth", models.PositiveIntegerField()),
                ("numchild", models.PositiveIntegerField(default=0)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="created at"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="updated at"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, max_length=255, verbose_name="name"
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_uk",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_pl",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", verbose_name="description"
                    ),
                ),
                (
                    "description_en",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "description_ru",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "description_uk",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "description_pl",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        db_index=True, default=True, verbose_name="active"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
            ],
            options={
                "verbose_name": "place category",
                "verbose_name_plural": "place categories",
            },
        ),
        migrations.CreateModel(
            name="Place",
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
                        auto_now=True, db_index=True, verbose_name="updated at"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, max_length=255, verbose_name="name"
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_uk",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_pl",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", verbose_name="description"
                    ),
                ),
                (
                    "description_en",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "description_ru",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "description_uk",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "description_pl",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        db_index=True, default=True, verbose_name="active"
                    ),
                ),
                (
                    "point",
                    django.contrib.gis.db.models.fields.PointField(
                        geography=True, srid=4326, verbose_name="point"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="places",
                        to="places.placecategory",
                        verbose_name="category",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
            ],
            options={
                "verbose_name": "place",
                "verbose_name_plural": "places",
                "ordering": ("-created_at",),
            },
            bases=(models.Model, django_admin_geomap.GeoItem),
        ),
        migrations.CreateModel(
            name="HistoricalPlaceCategory",
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
                ("path", models.CharField(db_index=True, max_length=255)),
                ("depth", models.PositiveIntegerField()),
                ("numchild", models.PositiveIntegerField(default=0)),
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
                    "name",
                    models.CharField(
                        db_index=True, max_length=255, verbose_name="name"
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_uk",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_pl",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", verbose_name="description"
                    ),
                ),
                (
                    "description_en",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "description_ru",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "description_uk",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "description_pl",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        db_index=True, default=True, verbose_name="active"
                    ),
                ),
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
            ],
            options={
                "verbose_name": "historical place category",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalPlace",
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
                    "name",
                    models.CharField(
                        db_index=True, max_length=255, verbose_name="name"
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_uk",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_pl",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", verbose_name="description"
                    ),
                ),
                (
                    "description_en",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "description_ru",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "description_uk",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "description_pl",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        db_index=True, default=True, verbose_name="active"
                    ),
                ),
                (
                    "point",
                    django.contrib.gis.db.models.fields.PointField(
                        geography=True, srid=4326, verbose_name="point"
                    ),
                ),
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
                    "category",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="places.placecategory",
                        verbose_name="category",
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
            ],
            options={
                "verbose_name": "historical place",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
