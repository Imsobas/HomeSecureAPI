# Generated by Django 3.1 on 2020-09-02 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0012_auto_20200902_0813'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PointCheckingCheckPointList',
            new_name='PointObservationCheckPointList',
        ),
    ]