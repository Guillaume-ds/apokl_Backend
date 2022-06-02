from rooms.models import Room, Post,Comment
from rest_framework import serializers
from creators.serializers import GetCreatorNameSerializer,GetCollectionPartialSerializer


class GetCommentSerializer(serializers.ModelSerializer):
    creatorInfo = serializers.SerializerMethodField('getCreator')
    class Meta:
        model = Comment
        fields = ["creatorInfo","content"]
    
    def getCreator(self,Comment):
        creator = Comment.creator
        serializedCreator = GetCreatorNameSerializer(creator)
        return serializedCreator.data

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'
 
class GetPostSerializer(serializers.ModelSerializer):  
    commentsInfo = serializers.SerializerMethodField('getComments')  
    class Meta:
        model = Post
        fields = ["id", "title", "content", "picture", "picture2", "creator", "collection","commentsInfo"]    
    
    def getComments(self,Post):
        comments = Comment.objects.filter(post=Post)
        serializedComments = GetCommentSerializer(comments,many=True)
        return serializedComments.data

class PostSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Post
        fields = '__all__'    
    
  
class RoomSerializer(serializers.ModelSerializer):
  creatorInfo = serializers.SerializerMethodField('getCreator')
  class Meta:
    model = Room
    fields = '__all__'
    
  def getCreator(self,Room):
    creator = Room.creator
    serializedCreator = GetCreatorNameSerializer(creator)
    return serializedCreator.data
  
class GetRoomSerializer(serializers.ModelSerializer):
    creatorInfo = serializers.SerializerMethodField('getCreator')
    collectionInfo = serializers.SerializerMethodField('getCollection')
    class Meta:
        model = Room
        fields = ["id","title","content","collectionInfo","creatorInfo","picture","picture2"]
        
    def getCreator(self,Room):
        creator = Room.creator
        serializedCreator = GetCreatorNameSerializer(creator)
        return serializedCreator.data
    
    def getCollection(self,Room):
        collection = Room.collection
        serializedCollection = GetCollectionPartialSerializer(collection)
        return serializedCollection.data

