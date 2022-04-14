from django.contrib.auth.models import User
from rest_framework.generics import RetrieveAPIView,CreateAPIView,UpdateAPIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from django.core.mail import send_mail
from accounts.serializers import UserSerializer,RegisterUserSerializer,ChangePasswordSerializer,ResetPasswordSerializer
import random
import string

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]
 
class RegisterUserAPIView(CreateAPIView):
	permission_classes = [permissions.AllowAny]
	serializer_class = RegisterUserSerializer

class UserAPIView(RetrieveAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user

class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User

    def get_user(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_user()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': ''
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordView(UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    model = User

    def post(self, request, *args, **kwargs):
        def random_password():
            characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(characters) for i in range(8))
            return password
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_exist = User.objects.filter(username=serializer.data.get("username")).exists()
            if user_exist == True:
                user = User.objects.get(username=serializer.data.get("username"))
                if serializer.data.get("email") == user.email:
                    password = random_password()
                    user.set_password(password)
                    send_mail(
                        'Apokl | Reset Password',
                        'Dear ' + user.username + ' This is your new password: ' + password,
                        'guillaumedesurville99@gmail.com',
                        [user.email],
                        fail_silently=False)
                    user.save()
                    response = {
                        'status': 'success',
                        'code': status.HTTP_200_OK,
                        'message': 'Password updated successfully',
                        'data': [user.username, user.email, password]
                    }
                    return Response(response)
                else:
                    return Response({"error": "Email adress doesn't exist"})
            else:
                return Response({"error": "User doesn't exist"})
        else:
            return Response({'error': 'Internal error'})