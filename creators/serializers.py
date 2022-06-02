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
class GetCreatorDetailsSerializer(serializers.ModelSerializer):
    collections = serializers.SlugRelatedField(many=True, read_only=True,slug_field='slug')
    nfts = serializers.SlugRelatedField(many=True, read_only=True,slug_field='tokenId')
    rooms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True) 
    class Meta:
        fields = '__all__'
        model = Creator
        
#4 view -> Retrieve specific Creator with partial data for context, only if user = creator 
class GetCreatorNameSerializer(serializers.ModelSerializer):       
    class Meta:
        fields = ['name','picture','id']
        model = Creator
        depth=1


"""--------------------------Collections---------------------------"""
#1 view -> allow to create a Creator + #3 view : update
class CreateCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'  
              
#2 view -> Retrieve all Collection with partial data  
class GetCollectionsSerializer(serializers.ModelSerializer):
    roomsCount = serializers.SerializerMethodField('countRooms')
    postsCount = serializers.SerializerMethodField('countPosts')
    creator = GetCreatorNameSerializer()
    class Meta:
        fields = ['id','name','slug',
                  'creator',
                  'description',
                  'tags','picture',
                  'nfts_array','roomsCount','postsCount']
        model = Collection
        lookup_field = 'creator'
    
    def countRooms(self,Collection):
        rooms = Room.objects.filter(collection=Collection.id).count()
        return rooms 
    
    def countPosts(self,Collection):
        posts = Post.objects.filter(creator=Collection.id).count()
        return posts
 
 
#3 view -> Retrieve all Collection with complete data        
class GetCollectionDetailsSerializer(serializers.ModelSerializer):
    rooms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        fields = '__all__'
        model = Collection
        lookup_field = 'creator'

#4 view -> Retrieve specific Collection with partial data for context
class GetCollectionPartialSerializer(serializers.ModelSerializer):       
    class Meta:
        fields = ['name','picture','slug']
        model = Collection
        depth=1