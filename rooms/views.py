from rest_framework import viewsets,permissions,status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rooms.serializers import PostSerializer,GetPostSerializer, RoomSerializer, CommentSerializer,GetCommentSerializer,GetRoomSerializer
from rooms.models import Room,Post,Comment
from creators.models import Collection,Creator
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

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
  serializer_class = GetRoomSerializer
  def get(self,request):
    return Response({"Error":"Wrong request"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
  def post(self,request):
    paginator = PageNumberPagination()
    paginator.page_size = 150
    
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
      postsSerialized = GetRoomSerializer(rooms,many=True)
      return paginator.get_paginated_response(postsSerialized.data)
    else:
      return Response({"Error":"Wrong address field"}, status=status.HTTP_400_BAD_REQUEST)


  
#3 view -> Claim Room 
class ClaimRoomAccessView(APIView):
  serializer_class = RoomSerializer
  permission_classes = [permissions.IsAuthenticated]
    
  def post(self, request, format=None):
    user = self.request.user
    try:
      if request.data['address'] and request.data['roomId']:
        try:
          room = Room.objects.get(id=int(request.data['roomId']))
          if request.data['address'] in room.addresses:
            try:
              """
              email = EmailMessage(
                'Apokl - Your exclusive room access ',
                f'Welcome {user.username}, you have access to {room.title}. More about this : {room.content}',
                'guillaumedesurville99@gmail.com',
                [user.email],
                headers={'Message-ID': 'foo'},
              )
              email.send()
              """
              to = user.email
              picture = room.collection.picture
              creator = room.creator.name
              print(creator,picture)
              html_content = render_to_string("room_email_template.html",
                                {'collectionImage':picture,
                                  'roomName':room.title,
                                  'content':room.content,
                                  'user':user.username,
                                  'creatorName':creator})
              text_content = strip_tags(html_content)
              index = room.addresses.index(request.data['address'])
              email = EmailMultiAlternatives(
                #subject : 
                "Apokl - Acces exclusive event",
                #content : 
                text_content,
                #from email
                settings.EMAIL_HOST_USER,
                #to:
                [to]                
              )
              email.attach_alternative(html_content,"text/html")
              email.send()
              print(settings.EMAIL_HOST_USER)
              room.addresses.pop(index)
              room.users.append(user.username)
              room.save(update_fields=['addresses','users'])
              return Response({'success': 'Message sent successfully'})
            except:
              return Response({'error': 'Message failed'}, status=status.HTTP_400_BAD_REQUEST)
          else:
            return Response({'error': 'User not allowed'}, status=status.HTTP_400_BAD_REQUEST)
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
    
    collection_id = request.data['collection']
    collection = Collection.objects.get(id=collection_id)
    if user == collection.creator.user:
      newPost = PostSerializer(data=request.data)
      if newPost.is_valid():
        newPost.save()
        return Response(newPost.data,status = status.HTTP_201_CREATED)
      else:
        return Response(newPost.error, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response({"Error":"User not allowed"}, status=status.HTTP_403_FORBIDDEN)
    
  
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
  serializer_class = GetPostSerializer
  
  def get(self,request):
    return Response({"Error":"Wrong request"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
  def post(self,request):
    paginator = PageNumberPagination()
    paginator.page_size = 50
    
    
    if request.data['collection']:
      collection_id = request.data['collection']
      collection = Collection.objects.get(id=collection_id)
      if request.data['access'] == 'true':
        posts = Post.objects.filter(collection=collection)
        serializer = GetPostSerializer(posts, many=True)
        result_page = paginator.paginate_queryset(serializer.data, request)    
        return paginator.get_paginated_response(result_page)
      else:
        return Response({"error":"You don't have access"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"Error":"Collection is not specified"}, status=status.HTTP_400_BAD_REQUEST)

    
    
    
      
"""--------------------------Comments---------------------------"""

#1 view -> allow to create a Post
class CommentViewSet(viewsets.ModelViewSet):
  queryset = Comment.objects.all()  
  permission_classes = (permissions.IsAuthenticated, )
  def create(self, request):
    user = self.request.user
    
    if request.data['access'] == "true":
      post = Post.objects.get(id=request.data['post'])
      if post.collection.id == request.data['collection']:
        creator = Creator.objects.get(user=user)
        request.data['creator'] = creator.id
        newComment = CommentSerializer(data=request.data)
        if newComment.is_valid():
          newComment.save()
          return Response(newComment.data,status = status.HTTP_201_CREATED)
        else:
          return Response({"Error":"Wrong data"}, status=status.HTTP_400_BAD_REQUEST)
      else:
        return Response({"Error":"Wrong data"}, status=status.HTTP_403_FORBIDDEN)
    else:
      return Response({"Error":"User not allowed"}, status=status.HTTP_403_FORBIDDEN)
    
    
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

#2 view -> Retrieve Comments for a specific post 
class GetCommentsView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = GetCommentSerializer
  
  def get(self,request):
    return Response({"Error":"Wrong request"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
  def post(self,request):
    paginator = PageNumberPagination()
    paginator.page_size = 50
    user = self.request.user
    
    if request.data['access'] == "true":
      post = Post.objects.get(id=request.data['post'])
      if post.collection.id == request.data['collection']:
        comments = Comment.objects.filter(post=post)
        result_page = paginator.paginate_queryset(comments, request)
        postsSerialized = GetCommentSerializer(comments,many=True)
        return paginator.get_paginated_response(postsSerialized.data)
      else:
        return Response({"Error":"Wrong data"}, status=status.HTTP_403_FORBIDDEN)
    else:
      return Response({"Error":"User not allowed"}, status=status.HTTP_403_FORBIDDEN)
   



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









