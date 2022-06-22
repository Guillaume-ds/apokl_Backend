from django.contrib.auth.models import Group
from profiles.models import Profile
from nfts.models import NFT
from profiles.serializers import GetProfileNameSerializer
from rest_framework import serializers


class NFTReadSerializer(serializers.ModelSerializer):
    creatorInfo = serializers.SerializerMethodField('getCreator')
    class Meta:
        fields = ["tokenId","title","is_published","creatorInfo","description","create_at","rarity","price","royalties"]
        model = NFT
        depth=1
        
    def getCreator(self,Comment):
        creator = Comment.creator
        serializedCreator = GetProfileNameSerializer(creator)
        return serializedCreator.data

class NFTWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = ['price','rarity','creator','title','description',"tokenId","royalties","tags"]


		
	