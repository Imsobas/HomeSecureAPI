# Generated by Django 3.1 on 2020-08-21 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='home_village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village'),
        ),
    ]
