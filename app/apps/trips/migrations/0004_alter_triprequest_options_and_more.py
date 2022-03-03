# Generated by Django 4.0.3 on 2022-03-03 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0003_alter_triprequest_updated_at"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="triprequest",
            options={
                "ordering": ("-route_length", "-created_at"),
                "verbose_name": "trip",
                "verbose_name_plural": "trips",
            },
        ),
        migrations.AddField(
            model_name="historicaltriprequest",
            name="route_length",
            field=models.FloatField(default=1, verbose_name="route_length"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="triprequest",
            name="route_length",
            field=models.FloatField(default=1, verbose_name="route_length"),
            preserve_default=False,
        ),
    ]
