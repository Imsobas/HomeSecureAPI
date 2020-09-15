# Generated by Django 3.1 on 2020-09-12 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0044_auto_20200912_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('company_address', models.CharField(blank=True, max_length=100, null=True)),
                ('company_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]