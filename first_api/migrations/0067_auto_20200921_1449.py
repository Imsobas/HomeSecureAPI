# Generated by Django 3.1 on 2020-09-21 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0066_auto_20200921_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generaluser',
            name='gen_user_username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]