from rest_framework import serializers
from profiles.serializers import GetProfileNameSerializer
from .models import Collection
from events.models import Event
from postsAndComments.models import Post

"""--------------------------Collections---------------------------"""
#1 view -> allow to create a Profile + #3 view : update
class CreateCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'  
              
#2 view -> Retrieve all Collection with partial data  
class GetCollectionsSerializer(serializers.ModelSerializer):
    eventsCount = serializers.SerializerMethodField('countEvents')
    postsCount = serializers.SerializerMethodField('countPosts')
    creator = GetProfileNameSerializer()
    class Meta:
        fields = ['id','name','slug',
                  'creator',
                  'description',
                  'tags','picture',
                  'nfts_array','eventsCount','postsCount']
        model = Collection
        lookup_field = 'creator'
    
    def countEvents(self,Collection):
        events = Event.objects.filter(collection=Collection.id).count()
        return events 
    
    def countPosts(self,Collection):
        posts = Post.objects.filter(collection=Collection.id).count()
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