# Generated by Django 3.1 on 2020-08-30 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0007_auto_20200829_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='work_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
