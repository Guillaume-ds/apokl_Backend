from django.contrib.auth.models import Group
from creators.models import Creator
from nfts.models import NFT
from creators.serializers import GetCreatorNameSerializer
from rest_framework import serializers


class NFTReadSerializer(serializers.ModelSerializer):
    creator =  GetCreatorNameSerializer()
    class Meta:
        fields = ["tokenId","title","is_published","creator","description","create_at","rarity","price","royalties"]
        model = NFT
        depth=1

class NFTWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = ['price','rarity','creator','title','description',"tokenId","royalties","tags"]


		
	