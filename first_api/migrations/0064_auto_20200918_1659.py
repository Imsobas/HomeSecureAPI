# Generated by Django 3.1 on 2020-09-18 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0063_auto_20200918_1516'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='voterecord',
            unique_together=set(),
        ),
    ]