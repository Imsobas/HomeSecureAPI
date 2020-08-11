from rest_framework import serializers

from first_api import models

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

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile objecft"""

    class Meta:
        model = models.UserProfile
        fields = ('id','email','name','password')
        extra_kwargs = {
             'password':{
                 'write_only': True,
                 'style': {'input_type': 'password'}
             }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user 