from venv import create
from .models import Creator, Collection
from .serializers import CreateCreatorSerializer,GetCreatorsSerializer,GetCreatorSerializer,CreateCollectionSerializer,GetCollectionSerializer
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
            return CreateCreatorSerializer
        else:
            return GetCreatorsSerializer 

#2 view -> Retrieve all Creator with partial data 
class SearchCreator(ListAPIView):  
  serializer_class = GetCreatorsSerializer        
  def post(self, request, format=None):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    
    queryset= Creator.objects.all()
    try:
      if request.data['tags'] != []:
        queryset = queryset.filter(tags__contains=request.data['tags'])
    except: None 
    
    try:
      if request.data['name'] != '':
        queryset = queryset.filter(name=request.data['name'])      
    except: None
    
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = GetCreatorSerializer(queryset, many=True)
    return paginator.get_paginated_response(serializer.data)
  
#3 view -> Retrieve specific Creator with complete data, only if user = creator  
class GetCreatorView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated, )
  serializer_class = GetCreatorSerializer
  
  def post(self,request):
    user = self.request.user
    try:
      creator = Creator.objects.get(user=user)
      serializer = GetCreatorSerializer(creator)
      return Response(serializer.data, status = status.HTTP_200_OK)
    except:
      return Response({"error":"No creator"},status=status.HTTP_400_BAD_REQUEST)   

#4 view -> Update Creator data
class UpdateCreatorView(APIView):    
  serializer_class = CreateCreatorSerializer 
  permission_classes = (permissions.IsAuthenticated, )  
    
  def put(self, request, format=None):   
    user = self.request.user
    creator = Creator.objects.get(user=user) 
    serializer = CreateCreatorSerializer(creator, data=request.data)    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

  

  
  
"""---------------------Collections--------------------"""

#1 view -> allow to create a Collection
class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()  
    permission_classes = (permissions.IsAuthenticated, )
    def get_serializer_class(self):
        if self.request.method == 'POST':
          try:
            return CreateCollectionSerializer
          except:
            return Response({"error":"Error occured, impossible to create this collection"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return GetCollectionSerializer 
  
  
class CollectionsView(ListAPIView):
  serializer_class = GetCollectionSerializer
  lookup_field = 'creator'  
  def get_queryset(self):
    name = self.kwargs['name']
    creator = Creator.objects.filter(name=name)
    return Collection.objects.filter(creator=creator)
      
class GetCollectionView(ListAPIView):
  serializer_class = GetCollectionSerializer
  lookup_field = 'creator'
  def get_queryset(self):
      name = self.kwargs['name']
      slug = self.kwargs['slug']
      return Collection.objects.filter(creator=name).filter(slug=slug)
      
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
      
class SearchCollection(ListAPIView):  
  serializer_class = GetCollectionSerializer        
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
    except: None  
    
    try:   
      if request.data['keywords'] != '':
        keywords = request.data['keywords']
        queryset = queryset.filter(description__icontains=keywords)
    except: None 
    
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = GetCollectionSerializer(queryset, many=True)
    return paginator.get_paginated_response(serializer.data)
  


