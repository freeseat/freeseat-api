# Generated by Django 4.0.3 on 2022-03-03 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_usersession_last_active_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicaluser",
            name="password",
            field=models.CharField(max_length=128, verbose_name="password"),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=128, verbose_name="password"),
        ),
    ]
