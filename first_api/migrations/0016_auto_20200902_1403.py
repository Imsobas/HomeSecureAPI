# Generated by Django 3.1 on 2020-09-02 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0015_auto_20200902_0826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pointobservation',
            name='observation_hour_split',
        ),
        migrations.AddField(
            model_name='pointobservationrecord',
            name='observation_timeslot',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='work',
            name='work_hour_split',
            field=models.IntegerField(default=0),
        ),
    ]