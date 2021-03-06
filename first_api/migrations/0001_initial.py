# Generated by Django 3.1 on 2020-12-24 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('user_role', models.CharField(choices=[('Admin', 'Admin'), ('Manager', 'Manager'), ('SecureBoss', 'SecureBoss'), ('SecureGuard', 'SecureGuard'), ('GeneralUser', 'GeneralUser')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CheckinCheckpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_name', models.CharField(max_length=100)),
                ('point_active', models.BooleanField(default=True)),
                ('point_lat', models.DecimalField(decimal_places=8, default=0.0, max_digits=11)),
                ('point_lon', models.DecimalField(decimal_places=8, default=0.0, max_digits=11)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
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
        migrations.CreateModel(
            name='GeneralUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gen_user_firstname', models.CharField(max_length=100)),
                ('gen_user_lastname', models.CharField(max_length=100)),
                ('gen_user_type', models.CharField(choices=[('ลูกบ้าน', 'ลูกบ้าน'), ('กรรมการหมู่บ้าน', 'กรรมการหมู่บ้าน'), ('ผู้ดูแลหมู่บ้าน', 'ผู้ดูแลหมู่บ้าน')], max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('gen_user_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company')),
            ],
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_number', models.CharField(blank=True, max_length=100, null=True)),
                ('home_address', models.CharField(blank=True, max_length=200, null=True)),
                ('home_lat', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('home_lon', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('house_space', models.FloatField(blank=True, null=True)),
                ('home_vote_qouta', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('home_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceFeePeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_period_name', models.CharField(max_length=100)),
                ('fee_start', models.DateField(blank=True, null=True)),
                ('fee_end', models.DateField(blank=True, null=True)),
                ('fee_deadline', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SecureGuard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secure_firstname', models.CharField(max_length=100)),
                ('secure_lastname', models.CharField(max_length=100)),
                ('secure_type', models.CharField(choices=[('หัวหน้า', 'หัวหน้า'), ('ขาเข้า', 'ขาเข้า'), ('ขาออก', 'ขาออก'), ('ในหมู่บ้าน', 'ในหมู่บ้าน')], max_length=100)),
                ('secure_join_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('secure_left_date', models.DateTimeField(blank=True, null=True)),
                ('secure_work_start_time', models.DateTimeField(blank=True, null=True)),
                ('secure_work_end_time', models.DateTimeField(blank=True, null=True)),
                ('secure_now_latitude', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('secure_now_lontitude', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('secure_now_location_time', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('secure_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company')),
                ('secure_username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('village_name', models.CharField(max_length=100)),
                ('village_address', models.CharField(blank=True, max_length=200, null=True)),
                ('village_lat', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('village_lon', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('village_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company')),
            ],
        ),
        migrations.CreateModel(
            name='VoteChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_thai_choice', models.CharField(blank=True, max_length=100, null=True)),
                ('vote_eng_choice', models.CharField(blank=True, max_length=100, null=True)),
                ('vote_chinese_choice', models.CharField(blank=True, max_length=100, null=True)),
                ('vote_is_result', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_name', models.CharField(max_length=100)),
                ('work_start_time', models.TimeField(blank=True, null=True)),
                ('work_end_time', models.TimeField(blank=True, null=True)),
                ('work_hour_split', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('work_village', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village')),
            ],
            options={
                'unique_together': {('work_name', 'work_village')},
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone_name', models.CharField(max_length=100)),
                ('zone_number', models.IntegerField(default=0)),
                ('zone_lat', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('zone_lon', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('zone_last_update', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('zone_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company')),
                ('zone_village', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village')),
            ],
        ),
        migrations.CreateModel(
            name='WorkingRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('working_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('working_in_out', models.CharField(blank=True, choices=[('เข้า', 'เข้า'), ('ออก', 'ออก')], max_length=5, null=True)),
                ('working_device', models.CharField(blank=True, max_length=100, null=True)),
                ('work_checkin_checkpoint', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.checkincheckpoint')),
                ('working_secure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.secureguard')),
                ('working_village', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village')),
                ('working_work', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.work')),
                ('working_zone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.zone')),
            ],
        ),
        migrations.CreateModel(
            name='VoteTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_thai_topic', models.CharField(blank=True, max_length=100, null=True)),
                ('vote_thai_detail', models.CharField(blank=True, max_length=400, null=True)),
                ('vote_eng_topic', models.CharField(blank=True, max_length=100, null=True)),
                ('vote_chinese_topic', models.CharField(blank=True, max_length=100, null=True)),
                ('vote_start_date', models.DateField(blank=True, null=True)),
                ('vote_end_date', models.DateField(blank=True, null=True)),
                ('vote_confirm_status', models.BooleanField(default=False)),
                ('vote_max_choice', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('vote_village', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village')),
            ],
        ),
        migrations.CreateModel(
            name='VoteRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_hiden', models.BooleanField(default=False)),
                ('vote_home', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.home')),
                ('vote_selected_choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.votechoice')),
                ('vote_topic_pk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.votetopic')),
                ('vote_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.generaluser')),
            ],
        ),
        migrations.AddField(
            model_name='votechoice',
            name='vote_topic_pk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.votetopic'),
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scan_waiting_duration', models.IntegerField(default=10)),
                ('qr_scaninTime_duration', models.IntegerField(default=6)),
                ('pointobservation_scan_distance', models.IntegerField(default=25)),
                ('checkin_scan_distance', models.IntegerField(default=25)),
                ('qr_scan_distance', models.IntegerField(default=25)),
                ('setting_village', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village')),
            ],
        ),
        migrations.CreateModel(
            name='SecureLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secure_location_type', models.CharField(blank=True, max_length=30, null=True)),
                ('secure_location_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('secure_lat', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('secure_lon', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('secure_pk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.secureguard')),
            ],
        ),
        migrations.AddField(
            model_name='secureguard',
            name='secure_village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village'),
        ),
        migrations.AddField(
            model_name='secureguard',
            name='secure_work_shift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.work'),
        ),
        migrations.AddField(
            model_name='secureguard',
            name='secure_zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.zone'),
        ),
        migrations.CreateModel(
            name='Qrcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_content', models.CharField(blank=True, max_length=200, null=True)),
                ('qr_type', models.CharField(blank=True, max_length=20, null=True)),
                ('qr_car_number', models.CharField(max_length=10)),
                ('qr_home_number', models.CharField(max_length=20)),
                ('qr_car_color', models.CharField(max_length=20)),
                ('qr_car_brand', models.CharField(max_length=20)),
                ('qr_enter_time', models.DateTimeField(blank=True, null=True)),
                ('qr_inside_time', models.DateTimeField(blank=True, null=True)),
                ('qr_home_time', models.DateTimeField(blank=True, null=True)),
                ('qr_exit_time', models.DateTimeField(blank=True, null=True)),
                ('qr_enter_status', models.BooleanField(default=False)),
                ('qr_inside_status', models.BooleanField(default=False)),
                ('qr_home_status', models.BooleanField(default=False)),
                ('qr_exit_status', models.BooleanField(default=False)),
                ('qr_enter_lat', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('qr_enter_lon', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('qr_inside_lat', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('qr_inside_lon', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('qr_home_lat', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('qr_home_lon', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('qr_exit_lat', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('qr_exit_lon', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('qr_detail', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('qr_livehome_status', models.BooleanField(blank=True, default=None, null=True)),
                ('qr_complete_status', models.BooleanField(default=False)),
                ('qr_exit_without_enter', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('qr_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company')),
                ('qr_enter_secure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='qr_enter_secure', to='first_api.secureguard')),
                ('qr_exit_secure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='qr_exit_secure', to='first_api.secureguard')),
                ('qr_home', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.home')),
                ('qr_inside_secure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='qr_inside_secure', to='first_api.secureguard')),
                ('qr_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.generaluser')),
                ('qr_village', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village')),
                ('qr_zone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.zone')),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('problem_type', models.CharField(blank=True, max_length=100, null=True)),
                ('problem_detail', models.CharField(blank=True, max_length=400, null=True)),
                ('problem_feedback', models.CharField(blank=True, max_length=400, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_active_admin', models.BooleanField(default=True)),
                ('problem_home', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.home')),
                ('problem_village', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village')),
            ],
        ),
        migrations.CreateModel(
            name='PointObservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observation_date', models.CharField(max_length=10)),
                ('observation_work_start_time', models.TimeField(blank=True, null=True)),
                ('observation_work_end_time', models.TimeField(blank=True, null=True)),
                ('observation_secure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.secureguard')),
                ('observation_village', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village')),
                ('observation_work', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.work')),
                ('observation_zone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.zone')),
            ],
            options={
                'unique_together': {('observation_village', 'observation_zone', 'observation_work', 'observation_secure', 'observation_date')},
            },
        ),
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
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_level', models.CharField(choices=[('VILLAGELEVEL', 'VILLAGELEVEL'), ('COMPANYLEVEL', 'COMPANYLEVEL')], max_length=100)),
                ('manager_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company')),
                ('manager_username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('manager_village', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceFeeRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_paid_date', models.DateField(blank=True, null=True)),
                ('fee_house_space', models.FloatField(blank=True, null=True)),
                ('fee_amount', models.FloatField(blank=True, null=True)),
                ('fee_paid_status', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('fee_home', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.home')),
                ('fee_period', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.maintenancefeeperiod')),
            ],
        ),
        migrations.AddField(
            model_name='maintenancefeeperiod',
            name='fee_village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village'),
        ),
        migrations.AddField(
            model_name='home',
            name='home_village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village'),
        ),
        migrations.AddField(
            model_name='home',
            name='home_zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.zone'),
        ),
        migrations.AddField(
            model_name='generaluser',
            name='gen_user_home',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.home'),
        ),
        migrations.AddField(
            model_name='generaluser',
            name='gen_user_username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='generaluser',
            name='gen_user_village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village'),
        ),
        migrations.AddField(
            model_name='generaluser',
            name='gen_user_zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.zone'),
        ),
        migrations.CreateModel(
            name='CustomFCMDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('active', models.BooleanField(default=True, help_text='Inactive devices will not be sent notifications', verbose_name='Is active')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation date')),
                ('device_id', models.CharField(blank=True, db_index=True, help_text='Unique device identifier', max_length=150, null=True, verbose_name='Device ID')),
                ('registration_id', models.TextField(verbose_name='Registration token')),
                ('type', models.CharField(choices=[('ios', 'ios'), ('android', 'android'), ('web', 'web')], max_length=10)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'FCM device',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Checkpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_name', models.CharField(max_length=100)),
                ('point_active', models.BooleanField(default=True)),
                ('point_lat', models.DecimalField(decimal_places=8, default=0.0, max_digits=11)),
                ('point_lon', models.DecimalField(decimal_places=8, default=0.0, max_digits=11)),
                ('is_active', models.BooleanField(default=True)),
                ('point_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company')),
                ('point_village', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village')),
                ('point_zone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.zone')),
            ],
        ),
        migrations.AddField(
            model_name='checkincheckpoint',
            name='point_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.company'),
        ),
        migrations.AddField(
            model_name='checkincheckpoint',
            name='point_village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.village'),
        ),
        migrations.CreateModel(
            name='VoteCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_count', models.IntegerField(default=0)),
                ('vote_home', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.home')),
                ('vote_topic_pk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.votetopic')),
            ],
            options={
                'unique_together': {('vote_home', 'vote_topic_pk')},
            },
        ),
        migrations.CreateModel(
            name='SecureWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secure_pk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.secureguard')),
                ('work_pk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.work')),
            ],
            options={
                'unique_together': {('secure_pk', 'work_pk')},
            },
        ),
        migrations.CreateModel(
            name='PointObservationRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observation_checkin_time', models.DateTimeField(blank=True, null=True)),
                ('observation_checkout_time', models.DateTimeField(blank=True, null=True)),
                ('observation_timeslot', models.IntegerField(default=0)),
                ('checkpoint_pk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.checkpoint')),
                ('observation_pk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.pointobservation')),
            ],
            options={
                'unique_together': {('observation_pk', 'observation_timeslot', 'checkpoint_pk')},
            },
        ),
        migrations.CreateModel(
            name='PointObservationPointList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkpoint_pk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.checkpoint')),
                ('observation_pk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first_api.pointobservation')),
            ],
            options={
                'unique_together': {('observation_pk', 'checkpoint_pk')},
            },
        ),
    ]
