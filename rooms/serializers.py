from rooms.models import Room, Post,Comment
from rest_framework import serializers
 
class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = '__all__'
  
class RoomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = '__all__'
  
class GetRoomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = ["id","title","content","creator","collection"]

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'