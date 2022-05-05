from rest_framework import viewsets,permissions,status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rooms.serializers import PostSerializer, RoomSerializer, CommentSerializer
from rooms.models import Room,Post,Comment
from creators.models import Collection
from django.core.mail import EmailMessage

"""--------------------------Rooms---------------------------"""
#1 view -> allow to create a Room
class RoomViewSet(viewsets.ModelViewSet):
  queryset = Room.objects.all()  
  permission_classes = (permissions.IsAuthenticated, )
  def create(self, request):
    user = self.request.user
    try:
      collection_id = request.data['collection']
      collection = Collection.objects.get(id=collection_id)
      if user == collection.creator.user:
        request.data['creator'] = collection.creator.id
        newRoom = RoomSerializer(data=request.data)
        if newRoom.is_valid():
          newRoom.save()
          return Response(newRoom.data,status = status.HTTP_201_CREATED)
        else:
          return Response(newRoom.error, status=status.HTTP_400_BAD_REQUEST)
      else:
        return Response({"Error":"User not allowed"}, status=status.HTTP_403_FORBIDDEN)
    except:
      return Response({"Error":"Error occured while creating the room"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  def update(self, request, pk=None):
    response = {'message': 'Update function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)

  def partial_update(self, request, pk=None):
    response = {'message': 'Update function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)

  def destroy(self, request, pk=None):
    response = {'message': 'Delete function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)
  
  def list(self,request):
    response = {'message': 'List function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)

#2 view -> Retrieve Rooms for a specific collection / address
class GetRoomView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = RoomSerializer
  def get(self,request):
    return Response({"Error":"Wrong request"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
  def post(self,request):
    paginator = PageNumberPagination()
    paginator.page_size = 50
    try:
      if request.data['address']:
        rooms = Room.objects.filter(addresses__contains=request.data['address'])    
          
        if request.data['collectionId'] != "None":
          try:
            collectionId = request.data['collectionId']   
            collection = Collection.objects.get(id=collectionId)
            rooms = rooms.filter(collection=collection)
          except:
            return Response({"Error":"Wrong collection data"}, status=status.HTTP_400_BAD_REQUEST)
          
        result_page = paginator.paginate_queryset(rooms, request)
        postsSerialized = RoomSerializer(rooms,many=True)
        return paginator.get_paginated_response(postsSerialized.data)
      else:
        return Response({"Error":"Wrong address field"}, status=status.HTTP_400_BAD_REQUEST)
    except:
      return Response({"Error":"Wrong data"}, status=status.HTTP_400_BAD_REQUEST)

  
#3 view -> Claim Room 
class ClaimRoomAccessView(APIView):
  serializer_class = RoomSerializer
  permission_classes = [permissions.IsAuthenticated]
    
  def post(self, request, format=None):
    user = self.request.user
    try:
      if request.data['address'] and request.data['roomId']:
        try:
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
        except:
          return Response({"error":"No collection corresponding"}, status=status.HTTP_400_BAD_REQUEST)
      else:
        return Response({"Error":"Collection is not specified"}, status=status.HTTP_400_BAD_REQUEST)    
    except:
      return Response({"Error":"Missing fields"}, status=status.HTTP_400_BAD_REQUEST)    
    
    
    

"""--------------------------Posts---------------------------"""

#1 view -> allow to create a Post
class PostViewSet(viewsets.ModelViewSet):
  queryset = Post.objects.all()  
  permission_classes = (permissions.IsAuthenticated, )
  def create(self, request):
    user = self.request.user
    try:
      collection_id = request.data['collection']
      collection = Collection.objects.get(id=collection_id)
      if user == collection.creator.user:
        request.data['creator'] = collection.creator.id
        newPost = PostSerializer(data=request.data)
        if newPost.is_valid():
          newPost.save()
          return Response(newPost.data,status = status.HTTP_201_CREATED)
        else:
          return Response(newPost.error, status=status.HTTP_400_BAD_REQUEST)
      else:
        return Response({"Error":"User not allowed"}, status=status.HTTP_403_FORBIDDEN)
    except:
      return Response({"Error":"Error occured while creating the room"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  def update(self, request, pk=None):
    response = {'message': 'Update function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)

  def partial_update(self, request, pk=None):
    response = {'message': 'Update function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)

  def destroy(self, request, pk=None):
    response = {'message': 'Delete function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)
  
  def list(self,request):
    response = {'message': 'List function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)

#2 view -> Retrieve Posts for a specific collection 
class GetPostsView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = PostSerializer
  
  def get(self,request):
    return Response({"Error":"Wrong request"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
  def post(self,request):
    paginator = PageNumberPagination()
    paginator.page_size = 50
    
    try:
      if request.data['collection']:
        collection_id = request.data['collection']
        collection = Collection.objects.get(id=collection_id)
        if request.data['access'] == 'true':
          posts = Post.objects.filter(collection=collection)
          result_page = paginator.paginate_queryset(posts, request)
          postsSerialized = PostSerializer(posts,many=True)
          return paginator.get_paginated_response(postsSerialized.data)
        else:
          return Response({"error":"You don't have access"}, status=status.HTTP_401_UNAUTHORIZED)
      else:
          return Response({"Error":"Collection is not specified"}, status=status.HTTP_400_BAD_REQUEST)
    except:
      return Response({"error":"No collection corresponding"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
      
"""--------------------------Comments---------------------------"""

#1 view -> allow to create a Post
class CommentViewSet(viewsets.ModelViewSet):
  queryset = Comment.objects.all()  
  permission_classes = (permissions.IsAuthenticated, )
  def create(self, request):
    user = self.request.user
    try:
      if request.data['access'] == "true":
        post = Post.objects.get(id=request.data['post'])
        if post.collection.id == request.data['collection']:
          newComment = CommentSerializer(data=request.data)
          if newComment.is_valid():
            newComment.save()
            return Response(newComment.data,status = status.HTTP_201_CREATED)
          else:
            print(request.data)
            return Response(newComment.error, status=status.HTTP_400_BAD_REQUEST)
        else:
          return Response({"Error":"Wrong data"}, status=status.HTTP_403_FORBIDDEN)
      else:
        return Response({"Error":"User not allowed"}, status=status.HTTP_403_FORBIDDEN)
    except:
      return Response({"error":"No collection corresponding"}, status=status.HTTP_400_BAD_REQUEST)
    
  def update(self, request, pk=None):
    response = {'message': 'Update function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)

  def partial_update(self, request, pk=None):
    response = {'message': 'Update function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)

  def destroy(self, request, pk=None):
    response = {'message': 'Delete function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)
  
  def list(self,request):
    response = {'message': 'List function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)

#2 view -> Retrieve Posts for a specific collection 
class GetCommentsView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = CommentSerializer
  
  def get(self,request):
    return Response({"Error":"Wrong request"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
  def post(self,request):
    paginator = PageNumberPagination()
    paginator.page_size = 50
    user = self.request.user
    try:
      if request.data['access'] == "true":
        post = Post.objects.get(id=request.data['post'])
        if post.collection.id == request.data['collection']:
          comments = Comment.objects.filter(post=post)
          result_page = paginator.paginate_queryset(comments, request)
          postsSerialized = CommentSerializer(comments,many=True)
          return paginator.get_paginated_response(postsSerialized.data)
        else:
          return Response({"Error":"Wrong data"}, status=status.HTTP_403_FORBIDDEN)
      else:
        return Response({"Error":"User not allowed"}, status=status.HTTP_403_FORBIDDEN)
    except:
      return Response({"error":"No comment corresponding"}, status=status.HTTP_400_BAD_REQUEST)



#3 view -> Retrieve Posts for a specific person 
class GetPersonalCommentsView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = CommentSerializer
  
  def get(self,request):
    return Response({"Error":"Wrong request"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
  def post(self,request):
    paginator = PageNumberPagination()
    paginator.page_size = 50
    user = self.request.user
    try:
      comments = Comment.objects.filter(creator=user.creator)
      result_page = paginator.paginate_queryset(comments, request)
      postsSerialized = CommentSerializer(comments,many=True)
      return paginator.get_paginated_response(postsSerialized.data)
    except:
      return Response({"error":"No comment corresponding"}, status=status.HTTP_400_BAD_REQUEST)









