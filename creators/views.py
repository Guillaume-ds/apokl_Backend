from venv import create
from .models import Creator, Collection
from .serializers import CreateCreatorSerializer,GetCreatorsSerializer,GetCreatorSerializer,CreateCollectionSerializer,GetCollectionSerializer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions,status,viewsets
import operator
from functools import reduce

class CreatorsView(ListAPIView):
  queryset = Creator.objects.all()
  permission_classes = (permissions.AllowAny, )
  serializer_class = GetCreatorsSerializer
  
class GetCreatorView(ListAPIView):
  serializer_class = GetCreatorSerializer
  lookup_field = 'name'
  def get_queryset(self):
        name = self.kwargs['name']
        return Creator.objects.filter(name=name)

class CreateCreatorView(APIView):    
  serializer_class = CreateCreatorSerializer 
  permission_classes = (permissions.IsAuthenticated, )   
  def post(self, request, format=None): 
    user = self.request.user
    if request.data['name'] not in ["activate","create-collection"]: 
      request.data['name'] = user.username      
      serializer = CreateCreatorSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_200_OK)
      else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else: 
       return Response({"error":"unauthorized username"}, status=status.HTTP_400_BAD_REQUEST)
  
  def put(self, request, format=None):   
    user = self.request.user
    creator = Creator.objects.get(name=user.username) 
    request.data['name'] = user.username
    serializer = CreateCreatorSerializer(creator, data=request.data)    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class SearchCreator(APIView):  
  serializer_class = GetCreatorSerializer
  
  def post(self, request, format=None):
    queryset= Creator.objects.all()
    if request.data['tags'] != []:
      queryset = queryset.filter(tags__contains=request.data['tags'])
    if request.data['name'] != '':
      queryset = queryset.filter(name=request.data['name'])      
      
    serializer = GetCollectionSerializer(queryset, many=True)
    return Response(serializer.data)
  
  
class CollectionsView(ListAPIView):
  serializer_class = GetCollectionSerializer
  lookup_field = 'creator'  
  def get_queryset(self):
        name = self.kwargs['name']
        return Collection.objects.filter(creator=name)
      
class GetCollectionView(ListAPIView):
  serializer_class = GetCollectionSerializer
  lookup_field = 'creator'
  def get_queryset(self):
      name = self.kwargs['name']
      slug = self.kwargs['slug']
      return Collection.objects.filter(creator=name).filter(slug=slug)
      
class CreateCollectionView(APIView):
  queryset = Collection.objects.all()
  permission_classes = (permissions.IsAuthenticated, )  
  serializer_class = CreateCollectionSerializer
    
  def post(self, request, format=None): 
    user = self.request.user
    if request.data['name'] not in ["activate","create-collection"]: 
      request.data['creator'] = user.username   
      serializer = CreateCollectionSerializer(data=request.data) 
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_200_OK)
      else:
          return Response({"error":"wtong data"}, status=status.HTTP_400_BAD_REQUEST)
    else: 
       return Response({"error":"unauthorized username"}, status=status.HTTP_400_BAD_REQUEST)
  
  def put(self, request, format=None):   
    user = self.request.user
    collection = Collection.objects.get(slug=request.data['slug']) 
    request.data['creator'] = user.username
    listIds=request.data['nfts']
    request.data['nfts']=list(set(listIds))
    serializer = CreateCollectionSerializer(collection, data=request.data)    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
class SearchCollection(APIView):  
  serializer_class = GetCollectionSerializer
  
  def post(self, request, format=None):
    queryset= Collection.objects.all()
    if request.data['nfts'] != []:
      queryset = queryset.filter(nfts__contains=request.data['nfts'])
    if request.data['tags'] != []:
      queryset = queryset.filter(tags__contains=request.data['tags'])
    if request.data['creator'] != '':
      queryset = queryset.filter(creator=request.data['creator'])      
    if request.data['keywords'] != '':
      keywords = request.data['keywords']
      queryset = queryset.filter(description__icontains=keywords)
      
    serializer = GetCollectionSerializer(queryset, many=True)
    return Response(serializer.data)
  
  
"""Better queryset for pagination, however, it is not working..."""
  
class SearchCollection2(viewsets.ModelViewSet):
  model = Collection
  serializer_class = GetCollectionSerializer

  def get_queryset(self):
    creator = self.request.query_params.get('creator')
    nfts = self.request.query_params.get('nfts')
    tags = self.request.query_params.get('tags')
    keywords = self.request.query_params.get('keywords')
    
    queryset= Collection.objects.filter(nfts__contains=nfts,tags__contains=tags)
    if creator != '*' :
      queryset = queryset.filter(creator=creator)      
    if keywords != '*':
      queryset = queryset.filter(description__icontains=keywords)

    return queryset

