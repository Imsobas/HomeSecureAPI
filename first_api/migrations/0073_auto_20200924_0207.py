# Generated by Django 3.1 on 2020-09-23 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0072_auto_20200924_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='manger_level',
            field=models.CharField(choices=[('VILLAGELEVEL', 'VILLAGELEVEL'), ('COMPANYLEVEL', 'COMPANYLEVEL')], max_length=100),
        ),
    ]
