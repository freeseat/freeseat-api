# Generated by Django 4.0.3 on 2022-03-05 22:24

import uuid

import django.db.models.deletion
import packages.django.db.fields
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_historicaluser_password_alter_user_password"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactInformation",
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
                    "first_name",
                    models.CharField(
                        db_index=True, max_length=64, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        db_index=True, max_length=64, verbose_name="last name"
                    ),
                ),
                (
                    "phone_number",
                    packages.django.db.fields.PhoneNumberField(
                        db_index=True, max_length=16, verbose_name="phone number"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        db_index=True,
                        default="",
                        max_length=254,
                        verbose_name="email",
                    ),
                ),
            ],
            options={
                "verbose_name": "contact information",
                "verbose_name_plural": "contact information",
            },
        ),
        migrations.CreateModel(
            name="HistoricalContactInformation",
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
                    "first_name",
                    models.CharField(
                        db_index=True, max_length=64, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        db_index=True, max_length=64, verbose_name="last name"
                    ),
                ),
                (
                    "phone_number",
                    packages.django.db.fields.PhoneNumberField(
                        db_index=True, max_length=16, verbose_name="phone number"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        db_index=True,
                        default="",
                        max_length=254,
                        verbose_name="email",
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
                "verbose_name": "historical contact information",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
