from postsAndComments.models import Post,Comment
from rest_framework import serializers
from profiles.serializers import GetProfileNameSerializer
from collectionsNft.serializers import GetCollectionPartialSerializer


class GetCommentSerializer(serializers.ModelSerializer):
    creatorInfo = serializers.SerializerMethodField('getCreator')
    class Meta:
        model = Comment
        fields = ["creatorInfo","content"]
    
    def getCreator(self,Comment):
        creator = Comment.creator
        serializedCreator = GetProfileNameSerializer(creator)
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
    
  
