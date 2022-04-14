from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView
from nfts.serializers import NFTDetailSerializer,NFTReadSerializer,NFTWriteSerializer
from nfts.models import NFT

class NFTView(RetrieveAPIView):
  queryset = NFT.objects.order_by('-create_at')
  serializer_class = NFTDetailSerializer
  lookup_field = 'slug'

class NFTViewSet(viewsets.ModelViewSet):
    queryset = NFT.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'POST':
            return NFTWriteSerializer
        else:
            return NFTReadSerializer     

