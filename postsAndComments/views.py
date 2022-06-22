from rest_framework import viewsets,permissions,status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from postsAndComments.serializers import PostSerializer,GetPostSerializer,CommentSerializer,GetCommentSerializer
from postsAndComments.models import Post,Comment
from profiles.models import Profile
from collectionsNft.models import Collection
    

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
        creator = Profile.objects.get(user=user)
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
      comments = Comment.objects.filter(creator=user.profile)
      result_page = paginator.paginate_queryset(comments, request)
      postsSerialized = CommentSerializer(comments,many=True)
      return paginator.get_paginated_response(postsSerialized.data)
    except:
      return Response({"error":"No comment corresponding"}, status=status.HTTP_400_BAD_REQUEST)









