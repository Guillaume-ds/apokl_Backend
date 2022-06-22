from rest_framework import serializers
from .models import Profile
from events.models import Event
from postsAndComments.models import Post

"""--------------------------Profile---------------------------"""

#1 view -> allow to create a Creator + #4 view : update
class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

#2 view -> Retrieve all Creator with partial data 
class GetProfilesSerializer(serializers.ModelSerializer):    
    nfts = serializers.SlugRelatedField(many=True, read_only=True,slug_field='tokenId')
    collections = serializers.SlugRelatedField(many=True, read_only=True,slug_field='slug')
    eventsCount = serializers.SerializerMethodField('countEvents')
    postsCount = serializers.SerializerMethodField('countPosts')
        
    class Meta:
        fields = ['id','name',
                  'description',
                  'tags','picture',
                  'nfts','collections',
                  'eventsCount','postsCount',
                  'instagramUrl','twitterUrl','discordUrl','youtubeUrl']
        model = Profile
        depth=1
        
    def countEvents(self,Profile):
        events = Event.objects.filter(creator=Profile.id).count()
        return events 
    
    def countPosts(self,Profile):
        posts = Post.objects.filter(creator=Profile.id).count()
        return posts
    
#3 view -> Retrieve specific Profile with complete data, only if user = Profile 
class GetProfileDetailsSerializer(serializers.ModelSerializer):
    collections = serializers.SlugRelatedField(many=True, read_only=True,slug_field='slug')
    nfts = serializers.SlugRelatedField(many=True, read_only=True,slug_field='tokenId')
    rooms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True) 
    class Meta:
        fields = '__all__'
        model = Profile
        
#4 view -> Retrieve specific Profile with partial data for context, only if user = Profile 
class GetProfileNameSerializer(serializers.ModelSerializer):       
    class Meta:
        fields = ['name','picture']
        model = Profile
        depth=1

