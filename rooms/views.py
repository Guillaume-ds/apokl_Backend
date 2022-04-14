from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions
from rooms.serializers import GroupSerializer, RoomSerializer
from rooms.models import Room

 
class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	permission_classes = [permissions.IsAuthenticated]

class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	permission_classes = [permissions.IsAuthenticated]