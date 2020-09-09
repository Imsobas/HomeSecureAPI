# Generated by Django 3.1 on 2020-09-09 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0034_remove_voterecord_vote_village'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votetopic',
            name='vote_confirm_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='voterecord',
            unique_together={('vote_home', 'vote_topic_pk')},
        ),
    ]