# Generated by Django 3.1 on 2020-09-15 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0056_auto_20200916_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='qr_enter_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]