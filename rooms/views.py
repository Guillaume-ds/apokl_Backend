from rest_framework import viewsets,permissions,status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rooms.serializers import PostSerializer, RoomSerializer
from rooms.models import Room,Post
from creators.models import Collection

 
  
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


  
class SearchPost(viewsets.ModelViewSet):
  model = Post
  serializer_class = PostSerializer


class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	permission_classes = [permissions.IsAuthenticated]