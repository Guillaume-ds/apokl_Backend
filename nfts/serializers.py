from django.contrib.auth.models import Group
from nfts.models import NFT
from rest_framework import serializers

class NFTDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = '__all__'
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


		
	