from .models import Collection
from profiles.models import Profile
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions,status,viewsets
 
  
"""---------------------Collections--------------------"""

#1 view -> allow to create a Collection
class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()  
    permission_classes = (permissions.IsAuthenticated, )
    def get_serializer_class(self):
        if self.request.method == 'POST':
          try:
            creator_name = self.request.data['creator']
            creator = Profile.objects.get(name = creator_name)
            self.request.data['creator']=creator.id
            return CreateCollectionSerializer
          except:
            return Response({"Error":"Wrong id for the creator"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return GetCollectionsSerializer 

#2 view -> Retrieve all Collection with search fields 
class SearchCollection(ListAPIView):  
  serializer_class = GetCollectionsSerializer   
  
  def get(self,request):
    return Response({"error":"Wrong request"}, status=status.HTTP_400_BAD_REQUEST) 
      
  def post(self, request, format=None):
    paginator = PageNumberPagination()
    paginator.page_size = 50
    
    queryset= Collection.objects.all()
    try:
      if (request.data['nfts'] != [] and type(request.data['nfts'])==list):
        queryset = queryset.filter(nfts_array__contains=request.data['nfts'])
      else:None      
    except: None 

    try:  
      if (request.data['tags'] != None and type(request.data['tags'])==list):
        queryset = queryset.filter(tags__contains=request.data['tags'])
      else:
        None      
    except: None  

    try:
      if(request.data['creator'] != "" and type(request.data['creator'])==str):
        try:
          creator = Profile.objects.get(name=request.data['creator'])
          if creator != None:
            queryset = queryset.filter(creator=creator)  
          else:
            queryset = Collection.objects.none()      
        except ObjectDoesNotExist:
          queryset = Collection.objects.none() 
      else:
        None      
    except: None  
    
    try:   
      if request.data['keywords'] != None:
        keywords = request.data['keywords']
        queryset = queryset.filter(description__icontains=keywords)
      else:None      
    except: None  
    
    try:
      if (request.data['id'] != None and type(request.data['id'])==list):
        queryset = queryset.filter(id__in=request.data['id'])     
      else:None      
    except: None 
    
    try:   
      if request.data['slug'] != None:
        queryset = queryset.filter(slug=request.data['slug'])
    except: None
    
    serializer = GetCollectionsSerializer(queryset, many=True)
    result_page = paginator.paginate_queryset(serializer.data, request)    
    return paginator.get_paginated_response(result_page)

#3 view -> Retrieve specific collection with complete data, only if user = creator 
class GetCollectionDetailsView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated, )
  serializer_class = GetCollectionDetailsSerializer
  
  def post(self,request):
    user = self.request.user
    creator = Profile.objects.get(user=user)
    try:
      collection = Collection.objects.filter(creator=creator)
      serializer = GetCollectionDetailsSerializer(collection,many=True)
      return Response(serializer.data, status = status.HTTP_200_OK)
    except:
      return Response({"error":"No creator"},status=status.HTTP_400_BAD_REQUEST) 

#4 view -> Update Collection data
class UpdateCollectionView(APIView):
  queryset = Collection.objects.all()
  permission_classes = (permissions.IsAuthenticated, )  
  serializer_class = CreateCollectionSerializer
          
  def put(self, request, format=None):   
    user = self.request.user
    creator = Profile.objects.get(user=user) 
    collection = Collection.objects.get(slug=request.data['slug']) 
    if collection.creator == creator:
      serializer = CreateCollectionSerializer(collection, data=request.data)    
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error":"user not allowed to modify this collection"}, status=status.HTTP_400_BAD_REQUEST)
     