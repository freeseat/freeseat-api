# Generated by Django 4.0.3 on 2022-03-07 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0006_historicalpointofinterest_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalpointofinterest",
            name="url",
            field=models.URLField(blank=True, null=True, verbose_name="url"),
        ),
        migrations.AddField(
            model_name="pointofinterest",
            name="url",
            field=models.URLField(blank=True, null=True, verbose_name="url"),
        ),
    ]