# Generated by Django 3.1 on 2020-09-18 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0064_auto_20200918_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setting',
            name='inside_scan_duration',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='point_scan_distance',
        ),
        migrations.AddField(
            model_name='setting',
            name='checkin_scan_distance',
            field=models.IntegerField(default=25),
        ),
        migrations.AddField(
            model_name='setting',
            name='pointobservation_scan_distance',
            field=models.IntegerField(default=25),
        ),
        migrations.AddField(
            model_name='setting',
            name='qr_scan_distance',
            field=models.IntegerField(default=25),
        ),
        migrations.AddField(
            model_name='setting',
            name='qr_scaninTime_duration',
            field=models.IntegerField(default=6),
        ),
        migrations.AddField(
            model_name='setting',
            name='scan_waiting_duration',
            field=models.IntegerField(default=10),
        ),
    ]