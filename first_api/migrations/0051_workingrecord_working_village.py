# Generated by Django 3.1 on 2020-09-12 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0050_workingrecord_working_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='workingrecord',
            name='working_village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village'),
        ),
    ]