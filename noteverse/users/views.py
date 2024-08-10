from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import UserSerializer, LoginSerializer
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema

# @swagger_auto_schema(operation_description="partial_update description override", responses={404: 'slug not found'})


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer