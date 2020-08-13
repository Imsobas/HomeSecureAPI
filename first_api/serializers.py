from rest_framework import serializers

from first_api import models


## Home Secure main serializers 

class CompanySerializer(serializers.ModelSerializer):
    """Serializes company items"""
    class Meta:
        model = models.Company
        fields = ('id','company_name','company_address','company_phone','is_active')

class VillageSerializer(serializers.ModelSerializer):
    """Serializes village items"""
    class Meta:
        model = models.Village
        ## return value in request are missing if not fill in field
        ## also receive value from post 
        fields = ('id','village_name','village_address','village_company','village_lat','village_lon','is_active')

class ZoneSerializer(serializers.ModelSerializer):
    """Serializes zone items"""
    class Meta:
        model = models.Zone
        fields = ('id','zone_name','zone_number','zone_village','zone_lat','zone_lon','zone_last_update')

class HomeSerializer(serializers.ModelSerializer):
    """Serializes home items"""
    class Meta:
        model = models.Home
        fields = ('id','home_number','home_address','home_zone','home_lat','home_lon','is_active')


## User serializer

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile objecft"""

    class Meta:
        model = models.UserProfile
        fields = ('id','username','user_role','password')
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



class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""
    class Meta:
        model = models.ProfileFeedItem ## set this serializer to this model 
        fields = ('id','user_profile','status_text','created_on')
        extra_kwargs = { ## additional value
            'user_profile': {'read_only': True}
        }

class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    date = serializers.DateTimeField()

    ## doesn't need if use ModelSerializer 
    def create(self, validated_data):
        return models.Article.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.author = validated_data.get('author',instance.author)
        instance.email = validated_data.get('email',instance.email)
        instance.date = validated_data.get('date',instance.date)
        instance.save()
        
        return instance



class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)

