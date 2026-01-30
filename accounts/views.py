from http.client import HTTPResponse

from django.shortcuts import render
from django.template.context_processors import request
from rest_framework.generics import CreateAPIView
from .serializers import SignUpSerializer, ChangePasswordSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
from .utility import send_simple_email,check_email
from random import randint
from .models import VerifyCodes
class SignUpView(APIView):
    serializer_class = SignUpSerializer
    queryset = User
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        data = {
            'status': status.HTTP_201_CREATED,
            'username': serializer.data['username'],
            'message': 'Akkount yaratildi'
        }
        return Response(data=data)

        
class LoginView(APIView):
    def post(self, request):
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        
        user = User.objects.filter(username=username).first()
        if user is None:
            raise ValidationError({"status": status.HTTP_400_BAD_REQUEST, 'message': 'Bizda bunaqa user mavjud emas'})
        user = user.check_password(password)
        if not user:
            raise ValidationError({"status": status.HTTP_400_BAD_REQUEST, 'message': 'PArolingiz xato'})
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise ValidationError({"status": status.HTTP_400_BAD_REQUEST, 'message': 'Bizda bunaqa user mavjud emas'})
        
        refresh = RefreshToken.for_user(user)
        
        data = {
            'status': status.HTTP_200_OK,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Siz tizimga kirdingiz'
        }
        
        return Response(data=data)
        
        
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request):
        refresh = self.request.data.get('refresh_token')
        refresh = RefreshToken(refresh)
        refresh.blacklist()
        data = {
            'success': True,
            'message': 'Siz tizimdan chiqdingiz'
        }
        return Response(data)
        


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = self.request.user
        
        data = {
            'status': status.HTTP_200_OK,
            'username': user.username,
            'first_name': user.first_name
        }
        return Response(data)
    
    
class ProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        serializer = ProfileUpdateSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            
            data = {
                'status': status.HTTP_200_OK,
                'username': user.username,
                'first_name': user.first_name,
                'message': 'Malumotlar yangilandi'
            }
            return Response(data)
        data = {
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'ERROR'
        }
        return Response(data)
    
    
class ChangePasswordView(APIView):
    permission_classes=[permissions.IsAuthenticated, ]
    serializer_class=ChangePasswordSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data={
            'status':status.HTTP_200_OK,
            'message':'Parol yangilandi'
        }
        return Response(data)

# class Test(APIView):
#     permission_classes=[permissions.AllowAny, ]
#     def post(self, request):
#         code = self.request.data.get('code')
#         user = self.request.data.get('user_email')
#         if send_simple_email(user, code):
#
#             return Response({
#                 'success':True,
#                 'message': "Kodingiz yuborildi, emailni tekshiring! "
#             })


class ForgotView(APIView):
    permission_classes=[permissions.AllowAny, ]
    def post(self,request):
        email = self.request.data.get('email')
        email = check_email('email')
        if email:
            user=User.objects.filter(email=email).first()
            if user is None:
                raise ValidationError("Bu email mavjud emas")

            code=random.randint(1000,9999)
            VerifyCodes.objects.create(
                user=user,
                code=code
            )
            data={
                'status':status.HTTP_200_OK,
                'message': 'Kodingiz yuborildi'
            }
            return HTTPResponse(data)
        data = {
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Xato'
        }
        return HTTPResponse(data)

class ResetCodeView(APIView):
    pass



