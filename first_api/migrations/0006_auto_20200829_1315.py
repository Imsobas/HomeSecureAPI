# Generated by Django 3.1 on 2020-08-29 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0005_auto_20200829_1311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qrcode',
            old_name='qr_user_status',
            new_name='qr_home_status',
        ),
        migrations.RenameField(
            model_name='qrcode',
            old_name='qr_user_time',
            new_name='qr_home_time',
        ),
    ]
