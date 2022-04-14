from django.contrib.auth.models import Group
from rooms.models import Room
from rest_framework import serializers
 
class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ['url', 'name']
  
class RoomSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Room
		fields = '__all__'