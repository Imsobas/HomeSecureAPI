# Generated by Django 3.1 on 2020-09-15 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0054_workingrecord_working_zone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noti_read_status', models.BooleanField(default=False)),
                ('noti_general_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.generaluser')),
                ('noti_home', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.home')),
                ('noti_qr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.qrcode')),
            ],
        ),
    ]