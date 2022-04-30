from rooms.models import Room, Post
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