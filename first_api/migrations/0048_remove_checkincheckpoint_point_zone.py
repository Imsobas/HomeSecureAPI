# Generated by Django 3.1 on 2020-09-12 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0047_checkincheckpoint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkincheckpoint',
            name='point_zone',
        ),
    ]
