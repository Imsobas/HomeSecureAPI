# Generated by Django 3.1 on 2020-09-06 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0023_auto_20200906_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancefee',
            name='fee_paid_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='maintenancefeeperiod',
            name='fee_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='maintenancefeeperiod',
            name='fee_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='maintenancefeeperiod',
            name='fee_start',
            field=models.DateField(blank=True, null=True),
        ),
    ]
