# Generated by Django 3.1 on 2020-09-09 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0037_auto_20200910_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='is_active_admin',
            field=models.BooleanField(default=True),
        ),
    ]