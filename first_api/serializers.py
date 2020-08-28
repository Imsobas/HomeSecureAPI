from rest_framework import serializers

from first_api import models


## Home Secure main serializers 

class CompanySerializer(serializers.ModelSerializer):
    """Serializes company items"""
    class Meta:
        model = models.Company
        fields = ('pk','company_name','company_address','company_phone','is_active')

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
        fields = ('pk','home_number','home_address', 'home_company','home_village','home_zone','home_lat','home_lon','is_active')

class GeneralUserSerializer(serializers.ModelSerializer):
    """Serializes GeneralUser items"""
    class Meta:
        model = models.GeneralUser
        fields = ('pk','gen_user_firstname','gen_user_lastname','gen_user_username','gen_user_type', 'gen_user_company','gen_user_village','gen_user_zone','gen_user_home','is_active')

class CheckpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Checkpoint
        fields = ('pk', 'point_name', 'point_active', 'point_zone', 'point_company','point_village', 'point_lat', 'point_lon', 'is_active')

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Work
        fields =  ('pk', 'work_name', 'work_start_time', 'work_end_time', 'work_village', 'is_active')

class SecureGuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecureGuard
        fields = ('pk', 'secure_firstname', 'secure_lastname', 'secure_username', 'secure_type', 'secure_zone', 'secure_village', 'secure_company', 'secure_join_date', 'secure_left_date', 'secure_work_start_time', 'secure_work_end_time', 'secure_work_shift', 'secure_current_location', 'secure_current_location_time', 'is_active' )

## User serializer

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile objecft"""

    class Meta:
        model = models.UserProfile
        fields = ('pk','username','user_role','groups','password','is_active')
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


# class ProfileFeedItemSerializer(serializers.ModelSerializer):
#     """Serializes profile feed items"""
#     class Meta:
#         model = models.ProfileFeedItem ## set this serializer to this model 
#         fields = ('pk','user_profile','status_text','created_on')
#         extra_kwargs = { ## additional value
#             'user_profile': {'read_only': True}
#         }
