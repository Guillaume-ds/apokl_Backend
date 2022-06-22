from rest_framework import permissions,status,viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from nfts.serializers import NFTReadSerializer,NFTWriteSerializer
from nfts.models import NFT
from profiles.models import Profile


#1 view -> Create NFT 
class NFTViewSet(viewsets.ModelViewSet):
    queryset = NFT.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    def get_serializer_class(self):
        if self.request.method == 'POST':
          try:
            profile_name = self.request.data['creator']
            print(profile_name)
            creator = Profile.objects.get(name = profile_name)
            print(creator)
            self.request.data['creator']=creator.id
            return NFTWriteSerializer
          except:
            return Response({"Error":"Wrong id for the creator"}, status=status.HTTP_400_BAD_REQUEST)
        else:
          return NFTReadSerializer     
        
#2 view -> Retrieve all NFT with search fields 
class SearchNFT(ListAPIView):  
  serializer_class = NFTReadSerializer   
  
  def get(self,request):
    return Response({"error":"Wrong request"}, status=status.HTTP_400_BAD_REQUEST) 
      
  def post(self, request, format=None):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    
    queryset= NFT.objects.all()
    
    try:  
      if (request.data['priceMin'] != "" and type(request.data['priceMin'])==int):
        queryset = queryset.filter(price__gte=request.data['priceMin'])
    except: None 
    
    try:  
      if (request.data['priceMax'] != "" and type(request.data['priceMax'])==int):
        queryset = queryset.filter(price__lte=request.data['priceMax'])
    except: None 

    try:  
      if (request.data['tags'] != [] and type(request.data['tags'])==list):
        queryset = queryset.filter(tags__contains=request.data['tags'])
    except: None 

    try:
      if(request.data['creator'] != None):
        creator_name = self.request.data['creator']
        creator = Profile.objects.get(name = creator_name)
        queryset = queryset.filter(creator=creator)
      else:
        None
    except: queryset= NFT.objects.none() 
    
  
    try:
      if(request.data['id'] != [] ):
        queryset = queryset.filter(tokenId__in=request.data['id'])
    except: None 
    
    try:   
      if request.data['keywords'] != None:
        keywords = request.data['keywords']
        queryset = queryset.filter(description__icontains=keywords)
    except: None 
    
    serializer = NFTReadSerializer(queryset, many=True)
    result_page = paginator.paginate_queryset(serializer.data, request)    
    return paginator.get_paginated_response(result_page)


