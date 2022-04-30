from turtle import update
from django.core import serializers
from rest_framework import viewsets,permissions,status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rooms.serializers import PostSerializer, RoomSerializer,GetRoomSerializer
from rooms.models import Room,Post
from creators.models import Collection
from django.core.mail import send_mail,EmailMessage

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  
    permission_classes = (permissions.IsAuthenticated, )
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostSerializer
        else:
            return PostSerializer 

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()  
    permission_classes = (permissions.IsAuthenticated, )
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RoomSerializer
        else:
            return RoomSerializer
 
  
class GetPostsView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = PostSerializer
  lookup_field = 'slug'
  def get_queryset(self):
    slug = self.kwargs['slug']
    try:
      collection = Collection.objects.get(slug=slug)
      try:
        posts = Post.objects.filter(collection=collection)
        return posts
      except:
        return Post.objects.none() 
    except:
      return Post.objects.none()        


class CreatePostView(APIView):
  permission_classes = (permissions.IsAuthenticated, )  
  serializer_class = PostSerializer    
  def post(self, request, format=None): 
    user = self.request.user
    collection = Collection.objects.get(id=request.data['collection'])
    if collection.creator == user.username: 
      post = Post(
        title=request.data['title'],
        content = request.data['content'],
        creator = user,
        collection = collection,
        picture = request.data['picture'],
        picture2 = request.data['picture2']
      )
      post.save()
      serialized_post = serializers.serialize('json', [ post, ])
      return Response(serialized_post)
    else: 
       return Response({"error":"unauthorized username"}, status=status.HTTP_400_BAD_REQUEST)
     
class CreateRoomView(APIView):
  permission_classes = (permissions.IsAuthenticated, )  
  serializer_class = RoomSerializer
    
  def post(self, request, format=None): 
    user = self.request.user
    collection = Collection.objects.get(id=request.data['collection'])
    if collection.creator == user.username: 
      room = Room(
        title=request.data['title'],
        content = request.data['content'],
        creator = user,
        collection = collection,
        addresses = request.data['addresses'],
        users = request.data['users'],
        picture = request.data['picture'],
        picture2 = request.data['picture2']
      )
      room.save()
      serialized_room = serializers.serialize('json', [ room, ])
      return Response(serialized_room)
    else: 
       return Response({"error":"unauthorized username"}, status=status.HTTP_400_BAD_REQUEST)
     

class GetRoomView(ListAPIView):
  model = Room
  serializer_class = GetRoomSerializer
  def get_queryset(self):
    address = self.kwargs['slug']    
    queryset= Room.objects.filter(addresses__contains=[address])
    return queryset
  
class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	permission_classes = [permissions.IsAuthenticated]

class ClaimRoomAccessView(APIView):
  serializer_class = RoomSerializer
  permission_classes = [permissions.IsAuthenticated]
    
  def post(self, request, format=None):
    user = self.request.user
    room = Room.objects.get(id=request.data['roomId'])
    if request.data['address'] in room.addresses:
      try:
        email = EmailMessage(
          'Apokl - Your exclusive room access ',
          f'Welcome {user.username}, you have access to {room.title}. More about this : {room.content}',
          'guillaumedesurville99@gmail.com',
          [user.email],
          headers={'Message-ID': 'foo'},
        )
        email.send()
        index = room.addresses.index(request.data['address'])
        room.addresses.pop(index)
        room.users.append(user.username)
        room.save(update_fields=['addresses','users'])
        return Response({'success': 'Message sent successfully'})
      except:
        return Response({'error': 'Message failed'})
    else:
      return Response({'error': 'User not allowed'})








