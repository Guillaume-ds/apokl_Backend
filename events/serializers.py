from events.models import Event
from rest_framework import serializers
from profiles.serializers import GetProfileNameSerializer
from collectionsNft.serializers import GetCollectionPartialSerializer

  
class EventSerializer(serializers.ModelSerializer):
  creatorInfo = serializers.SerializerMethodField('getCreator')
  class Meta:
    model = Event
    fields = '__all__'
    
  def getCreator(self,Room):
    creator = Room.creator
    serializedCreator = GetProfileNameSerializer(creator)
    return serializedCreator.data
  
class GetEventSerializer(serializers.ModelSerializer):
    creatorInfo = serializers.SerializerMethodField('getCreator')
    collectionInfo = serializers.SerializerMethodField('getCollection')
    class Meta:
        model = Event
        fields = ["id","title","content","collectionInfo","creatorInfo","picture","picture2"]
        
    def getCreator(self,Event):
        creator = Event.creator
        serializedCreator = GetProfileNameSerializer(creator)
        return serializedCreator.data
    
    def getCollection(self,Event):
        collection = Event.collection
        serializedCollection = GetCollectionPartialSerializer(collection)
        return serializedCollection.data

