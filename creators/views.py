from .models import Creator, Collection
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions,status,viewsets


"""--------------------------Creators---------------------------"""

#1 view -> allow to create a Creator
class CreatorViewSet(viewsets.ModelViewSet):
    queryset = Creator.objects.all()  
    permission_classes = (permissions.IsAuthenticated, )
    def get_serializer_class(self):
        if self.request.method == 'POST':
          try:
            return CreateCreatorSerializer
          except:
            return Response({"error":"Error occured, impossible to create this creator"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return GetCreatorsSerializer 

#2 view -> Retrieve all Creator with partial data 
class SearchCreator(ListAPIView):  
  serializer_class = GetCreatorsSerializer   
  
  def get(self,request):
    return Response({"error":"Wrong request"}, status=status.HTTP_400_BAD_REQUEST)
       
  def post(self, request, format=None):
    paginator = PageNumberPagination()
    paginator.page_size = 50
    
    queryset= Creator.objects.all()
    try:
      if (request.data['tags'] != [] and type(request.data['tags'])==list):
        queryset = queryset.filter(tags__contains=request.data['tags'])
    except: None 
    
    try:
      if (request.data['name'] != '' and type(request.data['name'])==str):
        queryset = queryset.filter(name=request.data['name'])      
    except: None
    
    try:
      if (request.data['id'] != [] and type(request.data['id'])==list):
        queryset = queryset.filter(id__in=request.data['id'])      
    except: None
    
    serializer = GetCreatorsSerializer(queryset, many=True)
    result_page = paginator.paginate_queryset(serializer.data, request)    
    return paginator.get_paginated_response(result_page)
  
#3 view -> Retrieve specific Creator with complete data, only if user = creator  
class GetCreatorDetailsView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated, )
  serializer_class = GetCreatorDetailsSerializer
  
  def post(self,request):
    user = self.request.user
    
    creator = Creator.objects.get(user=user)
    serializer = GetCreatorDetailsSerializer(creator)
    return Response(serializer.data, status = status.HTTP_200_OK)
       
    
#4 view -> Retrieve specific Creator with complete data, only if user = creator  
class GetCreatorContextView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated, )
  serializer_class = GetCreatorsSerializer
  
  def post(self,request):
    user = self.request.user
    try:
      creator = Creator.objects.get(user=user)
      serializer = GetCreatorsSerializer(creator)
      return Response(serializer.data, status = status.HTTP_200_OK)
    except:
      return Response({"error":"No creator"},status=status.HTTP_400_BAD_REQUEST)

#5 view -> Update Creator data
class UpdateCreatorView(APIView):    
  serializer_class = CreateCreatorSerializer 
  permission_classes = (permissions.IsAuthenticated, )  
    
  def put(self, request, format=None):   
    user = self.request.user
    creator = Creator.objects.get(user=user) 
    serializer = CreateCreatorSerializer(creator, data=request.data)    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

  

  
  
"""---------------------Collections--------------------"""

#1 view -> allow to create a Collection
class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()  
    permission_classes = (permissions.IsAuthenticated, )
    def get_serializer_class(self):
        if self.request.method == 'POST':
          try:
            creator_name = self.request.data['creator']
            creator = Creator.objects.get(name = creator_name)
            self.request.data['creator']=creator.id
            print(self.request.data)
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
    paginator.page_size = 10
    
    queryset= Collection.objects.all()
    try:
      if (request.data['nfts'] != [] and type(request.data['nfts'])==list):
        queryset = queryset.filter(nfts__contains=request.data['nfts'])
    except: None 

    try:  
      if (request.data['tags'] != [] and type(request.data['tags'])==list):
        queryset = queryset.filter(tags__contains=request.data['tags'])
    except: None 

    try:
      if(request.data['creator'] != '' and type(request.data['creator'])==str):
        creator = Creator.objects.get(name=request.data['creator'])
        queryset = queryset.filter(creator=creator)        
    except: queryset = Collection.objects.none()  
    
    try:   
      if request.data['keywords'] != '':
        keywords = request.data['keywords']
        queryset = queryset.filter(description__icontains=keywords)
    except: None 
    
    try:
      if (request.data['id'] != [] and type(request.data['id'])==list):
        queryset = queryset.filter(id__in=request.data['id'])      
    except: None
    
    try:   
      if request.data['slug'] != '':
        queryset = queryset.filter(slug=request.data['slug'])
    except: None
    
    serializer = GetCollectionsSerializer(queryset, many=True)
    result_page = paginator.paginate_queryset(serializer.data, request)    
    return paginator.get_paginated_response(result_page)

#3 view -> Retrieve specific Creator with complete data, only if user = creator 
class GetCollectionDetailsView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated, )
  serializer_class = GetCollectionDetailsSerializer
  
  def post(self,request):
    user = self.request.user
    creator = Creator.objects.get(user=user)
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
    creator = Creator.objects.get(user=user) 
    collection = Collection.objects.get(slug=request.data['slug']) 
    if collection.creator == creator:
      serializer = CreateCollectionSerializer(collection, data=request.data)    
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error":"user not allowed to modify this collection"}, status=status.HTTP_400_BAD_REQUEST)
     

      

      

  


