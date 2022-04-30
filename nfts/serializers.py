from django.contrib.auth.models import Group
from creators.models import Creator
from nfts.models import NFT
from creators.serializers import GetCreatorNameSerializer
from rest_framework import serializers

class NFTDetailSerializer(serializers.ModelSerializer):
    creator =  GetCreatorNameSerializer()
    class Meta:
        model = NFT
        fields = ["tokenId","title","is_published","creator","description","create_at","rarity"]
        lookup_field = 'slug'

class NFTReadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = NFT
        depth=1
        lookup_field = 'slug'

class NFTWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = ['price','rarity','creator','title','description','slug']
        lookup_field = 'slug'


		
	