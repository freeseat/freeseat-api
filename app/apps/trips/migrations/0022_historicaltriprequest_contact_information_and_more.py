# Generated by Django 4.0.3 on 2022-03-07 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_contactinformation_first_name_and_more'),
        ('trips', '0021_alter_triprequest_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltriprequest',
            name='contact_information',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounts.contactinformation', verbose_name='contact_information'),
        ),
        migrations.AddField(
            model_name='triprequest',
            name='contact_information',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.contactinformation', verbose_name='contact_information'),
        ),
    ]
