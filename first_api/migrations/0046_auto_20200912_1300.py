# Generated by Django 3.1 on 2020-09-12 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0045_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkpoint',
            name='point_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company'),
        ),
        migrations.AddField(
            model_name='generaluser',
            name='gen_user_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company'),
        ),
        migrations.AddField(
            model_name='home',
            name='home_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company'),
        ),
        migrations.AddField(
            model_name='qrcode',
            name='qr_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company'),
        ),
        migrations.AddField(
            model_name='secureguard',
            name='secure_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company'),
        ),
        migrations.AddField(
            model_name='village',
            name='village_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company'),
        ),
        migrations.AddField(
            model_name='zone',
            name='zone_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company'),
        ),
    ]