from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['url', 'username', 'email', 'groups','id','date_joined']

class RegisterUserSerializer(serializers.HyperlinkedModelSerializer):
	def create(self, validated_data):
		user = User.objects.create_user(
			email = validated_data['email'],
			username = validated_data['username'],
			password = validated_data['password'])
		return user

	class Meta:
		model = User
		fields = ['url', 'username', 'password', 'email', 'groups']
  
class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    model = User
    email = serializers.CharField(required=True)
    username = serializers.CharField(required=True)