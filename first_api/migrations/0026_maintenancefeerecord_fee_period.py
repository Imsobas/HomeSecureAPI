# Generated by Django 3.1 on 2020-09-07 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0025_auto_20200906_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancefeerecord',
            name='fee_period',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.maintenancefeeperiod'),
        ),
    ]