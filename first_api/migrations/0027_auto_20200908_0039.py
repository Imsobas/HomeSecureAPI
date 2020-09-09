# Generated by Django 3.1 on 2020-09-07 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0026_maintenancefeerecord_fee_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenancefeerecord',
            name='fee_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='maintenancefeerecord',
            name='fee_house_space',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='maintenancefeerecord',
            name='fee_paid_status',
            field=models.BooleanField(default=False),
        ),
    ]