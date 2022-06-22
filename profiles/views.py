from .models import Profile
from .serializers import *

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions,status,viewsets


"""--------------------------Profile---------------------------"""

#1 view -> allow to create a Profile
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()  
    permission_classes = (permissions.IsAuthenticated, )
    def get_serializer_class(self):
        if self.request.method == 'POST':
          try:
            return CreateProfileSerializer
          except:
            return Response({"error":"Error occured, impossible to create this Profile"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return GetProfilesSerializer 

#2 view -> Retrieve all Profile with partial data 
class SearchProfile(ListAPIView):  
  serializer_class = GetProfilesSerializer   
  
  def get(self,request):
    return Response({"error":"Wrong request"}, status=status.HTTP_400_BAD_REQUEST)
       
  def post(self, request, format=None):
    paginator = PageNumberPagination()
    paginator.page_size = 50
    
    queryset= Profile.objects.all()
    try:
      if (request.data['tags'] != [] and type(request.data['tags'])==list):
        queryset = queryset.filter(tags__contains=request.data['tags'])
    except: None 
    
    try:
      if (request.data['name'] != '' and type(request.data['name'])==str):
        queryset = queryset.filter(name__contains=request.data['name'])   

    except: None
    
    try:
      if (request.data['id'] != [] and type(request.data['id'])==list):
        queryset = queryset.filter(id__in=request.data['id'])      
    except: None
    
    serializer = GetProfilesSerializer(queryset, many=True)
    result_page = paginator.paginate_queryset(serializer.data, request)    
    return paginator.get_paginated_response(result_page)
  
#3 view -> Retrieve specific Profile   
class GetSpecificProfileView(ListAPIView):
  
  serializer_class = GetProfilesSerializer
  queryset= Profile.objects.all()
  
  def get(self,request,creatorName):
    try:
      queryset = Profile.objects.get(name=creatorName)
      serializer = GetProfilesSerializer(queryset)
      return Response(serializer.data)
    except:      
      queryset = Profile.objects.none()
      return Response(None)
      
    
  
  
#4 view -> Retrieve specific Profile with complete data, only if user = Profile  
class GetProfileDetailsView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated, )
  serializer_class = GetProfileDetailsSerializer
  
  def post(self,request):
    user = self.request.user
    
    profile = Profile.objects.get(user=user)
    serializer = GetProfileDetailsSerializer(profile)
    return Response(serializer.data, status = status.HTTP_200_OK)
       
    
#5 view -> Retrieve specific Profile with complete data, only if user = Profile  
class GetProfileContextView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated, )
  serializer_class = GetProfilesSerializer
  
  def post(self,request):
    user = self.request.user
    try:
      profile = Profile.objects.get(user=user)
      serializer = GetProfilesSerializer(profile)
      return Response(serializer.data, status = status.HTTP_200_OK)
    except:
      return Response({"error":"No Profile"},status=status.HTTP_400_BAD_REQUEST)

#6 view -> Update Profile data
class UpdateProfileView(APIView):    
  serializer_class = CreateProfileSerializer 
  permission_classes = (permissions.IsAuthenticated, )  
    
  def put(self, request, format=None):   
    user = self.request.user
    profile = Profile.objects.get(user=user) 
    serializer = CreateProfileSerializer(profile, data=request.data)    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

  



      

      

  


