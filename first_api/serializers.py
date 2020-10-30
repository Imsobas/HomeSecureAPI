from rest_framework import serializers

from first_api import models


## Home Secure main serializers 

class CompanySerializer(serializers.ModelSerializer):
    """Serializes company items"""
    class Meta:
        model = models.Company
        fields = ('pk','company_name','company_address','company_phone','is_active')

class VillageSerializer(serializers.ModelSerializer):
    """Serializes village items"""
    class Meta:
        model = models.Village
        ## return value in request are missing if not fill in field
        ## also receive value from post 
        fields = ('pk','village_name','village_address','village_company','village_lat','village_lon','is_active')

class ZoneSerializer(serializers.ModelSerializer):
    """Serializes zone items"""
    class Meta:
        model = models.Zone
        fields = ('pk','zone_name','zone_number', 'zone_company','zone_village','zone_lat','zone_lon','zone_last_update','is_active')

class HomeSerializer(serializers.ModelSerializer):
    """Serializes home items"""
    class Meta:
        model = models.Home
        fields = ('pk','home_number','home_address', 'home_company','home_village','home_zone','home_lat','home_lon', 'house_space','home_vote_qouta','is_active')

class GeneralUserSerializer(serializers.ModelSerializer):
    """Serializes GeneralUser items"""
    class Meta:
        model = models.GeneralUser
        fields = ('pk','gen_user_firstname','gen_user_lastname','gen_user_username','gen_user_type', 'gen_user_company','gen_user_village','gen_user_zone','gen_user_home','is_active')

class CheckpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Checkpoint
        fields = ('pk', 'point_name', 'point_active', 'point_zone', 'point_company','point_village', 'point_lat', 'point_lon', 'is_active')

class CheckinCheckpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CheckinCheckpoint
        fields = ('pk', 'point_name', 'point_active','point_village', 'point_company', 'point_lat', 'point_lon', 'is_active')

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Work
        fields =  ('pk', 'work_name', 'work_start_time', 'work_end_time', 'work_hour_split', 'work_village', 'is_active')

class SecureGuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecureGuard
        fields = ('pk', 'secure_firstname', 'secure_lastname', 'secure_username', 'secure_type', 'secure_zone', 'secure_village', 'secure_company', 'secure_join_date', 'secure_left_date', 'secure_work_start_time', 'secure_work_end_time', 'secure_work_shift', 'secure_now_latitude', 'secure_now_lontitude', 'secure_now_location_time', 'is_active' )
    
class SecureLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecureLocation
        fields = ('pk', 'secure_pk', 'secure_location_type', 'secure_location_time', 'secure_lat', 'secure_lon')

class SecureWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecureWork
        fields = ('pk', 'secure_pk', 'work_pk')

class QrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Qrcode
        fields = ('pk', 'qr_content', 'qr_type', 'qr_car_number', 'qr_home_number',
         'qr_car_color', 'qr_car_brand', 'qr_company', 'qr_village', 'qr_zone',
          'qr_home', 'qr_user', 'qr_enter_secure', 'qr_inside_secure', 'qr_exit_secure', 
          'qr_enter_time', 'qr_inside_time', 'qr_home_time', 'qr_exit_time', 'qr_enter_status',
          'qr_inside_status', 'qr_home_status', 'qr_exit_status', 'qr_enter_lat', 'qr_enter_lon',
          'qr_inside_lat', 'qr_inside_lon', 
          'qr_home_lat', 'qr_home_lon', 
          'qr_exit_lat', 'qr_exit_lon','qr_detail', 'qr_livehome_status',
          'qr_complete_status', 'qr_exit_without_enter', 'is_active')

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Setting
        fields = ('pk', 'setting_village','scan_waiting_duration', 'qr_scaninTime_duration','pointobservation_scan_distance','checkin_scan_distance','qr_scan_distance')

    

# class PointInspectionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.PointInspection
#         fields = ('pk', 'inspect_checkin_time', 'inspect_checkout_time', 'inspect_checkpoint', 'inspect_village', 'inspect_zone', 'inspect_secure', 'insepect_work')

class PointObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PointObservation
        fields = ('pk', 'observation_village', 'observation_zone','observation_work','observation_secure','observation_date')

class PointObservationPointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PointObservationPointList
        fields = ('pk', 'observation_pk', 'checkpoint_pk')

class PointObservationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PointObservationRecord
        fields = ('pk', 'observation_pk', 'observation_checkin_time','observation_checkout_time', 'observation_timeslot','checkpoint_pk')

# class PointObservationRecordSerializer2(serializers.ModelSerializer):
#     class Meta: 
#         model = models.PointObservationRecord
#         fields = ('pk','observation_checkin_time', 'observation_checkout_time','observation_timeslot','checkpoint_pk')

class MaintenanceFeePeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MaintenanceFeePeriod
        fields = ('pk', 'fee_village', 'fee_period_name','fee_start', 'fee_end','fee_deadline','is_active')

class MaintenanceFeeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MaintenanceFeeRecord
        fields = ('pk', 'fee_period','fee_home', 'fee_paid_date','fee_house_space', 'fee_amount', 'fee_paid_status','is_active')

class VoteTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoteTopic
        fields = ('pk', 'vote_village','vote_thai_topic','vote_thai_detail', 'vote_eng_topic','vote_chinese_topic', 'vote_start_date', 'vote_end_date','vote_confirm_status','is_active')

class VoteChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoteChoice
        fields = ('pk', 'vote_topic_pk','vote_thai_choice', 'vote_eng_choice','vote_chinese_choice', 'vote_is_result', 'is_active')

class VoteRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoteRecord
        fields = ('pk', 'vote_topic_pk','vote_home', 'vote_user', 'vote_selected_choice','vote_hiden')

class VoteCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoteCount
        fields = ('pk', 'vote_topic_pk','vote_home', 'vote_count')


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Problem
        fields =('pk', 'problem_village','problem_home','problem_date','problem_type','problem_detail','problem_feedback', 'is_active', 'is_active_admin')
        
class WorkingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkingRecord
        fields =('pk', 'working_village', 'working_zone','working_secure','working_work', 'working_date','work_checkin_checkpoint','working_in_out','working_device')

class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomFCMDevice
        fields = ('pk','name','active','user', 'registration_id','date_created','device_id','type', )
     
        
## User serializer

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile objecft"""

    class Meta:
        model = models.UserProfile
        fields = ('pk','username','user_role','groups','password','is_active','is_staff')
        extra_kwargs = {
             'password':{
                 'write_only': True,
                 'style': {'input_type': 'password'}
             }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            username=validated_data['username'],
            user_role=validated_data['user_role'],
            password=validated_data['password']
        )

        return user 

class NotificationSerializer(serializers.ModelSerializer):
     """Notification Serializer for user profile objecft"""
     class Meta:
        model = models.Notification
        fields =('pk', 'noti_home', 'noti_general_user','noti_qr','noti_read_status')

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manager
        fields = ('pk','manager_username','manager_company','manager_village','manager_level')


# class ProfileFeedItemSerializer(serializers.ModelSerializer):
#     """Serializes profile feed items"""
#     class Meta:
#         model = models.ProfileFeedItem ## set this serializer to this model 
#         fields = ('pk','user_profile','status_text','created_on')
#         extra_kwargs = { ## additional value
#             'user_profile': {'read_only': True}
#         }
