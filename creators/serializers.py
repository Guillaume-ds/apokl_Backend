from rest_framework import serializers
from .models import Creator,Collection

class CreateCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = '__all__'

class GetCreatorsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Creator
        depth=1

class GetCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Creator
        lookup_field = 'name'

class CreateCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'        
        
class GetCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Collection
        lookup_field = 'creator'