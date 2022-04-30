from rest_framework import serializers
from .models import Creator,Collection
from rooms.models import Room, Post

"""--------------------------Creators---------------------------"""

#1 view -> allow to create a Creator + #4 view : update
class CreateCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = '__all__'

#2 view -> Retrieve all Creator with partial data 
class GetCreatorsSerializer(serializers.ModelSerializer):    
    nfts = serializers.SlugRelatedField(many=True, read_only=True,slug_field='tokenId')
    collections = serializers.SlugRelatedField(many=True, read_only=True,slug_field='slug')
    roomsCount = serializers.SerializerMethodField('countRooms')
    postsCount = serializers.SerializerMethodField('countPosts')
        
    class Meta:
        fields = ['id','name',
                  'description',
                  'tags','picture',
                  'nfts','collections',
                  'roomsCount','postsCount',
                  'instagramUrl','twitterUrl','discordUrl','youtubeUrl']
        model = Creator
        depth=1
        
    def countRooms(self,Creator):
        rooms = Room.objects.filter(creator=Creator.id).count()
        return rooms 
    
    def countPosts(self,Creator):
        posts = Post.objects.filter(creator=Creator.id).count()
        return posts
    
#3 view -> Retrieve specific Creator with complete data, only if user = creator 
class GetCreatorSerializer(serializers.ModelSerializer):
    collections = serializers.SlugRelatedField(many=True, read_only=True,slug_field='slug')
    nfts = serializers.SlugRelatedField(many=True, read_only=True,slug_field='tokenId')
    rooms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True) 
    class Meta:
        fields = '__all__'
        model = Creator
        

class GetCreatorNameSerializer(serializers.ModelSerializer):       
    class Meta:
        fields = ['name']
        model = Creator
        depth=1


"""--------------------------Collections---------------------------"""







class CreateCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'        
        
class GetCollectionSerializer(serializers.ModelSerializer):
    rooms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        fields = '__all__'
        model = Collection
        lookup_field = 'creator'