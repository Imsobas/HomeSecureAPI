# Generated by Django 3.1 on 2020-09-18 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0061_home_house_space'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='home_vote_couta',
            field=models.IntegerField(default=1),
        ),
    ]