from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import UserSerializer, LoginSerializer
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response

# @swagger_auto_schema(operation_description="partial_update description override", responses={404: 'slug not found'})


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    
    

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
    
#     def get_queryset(self):
#         queryset = get_user_model().objects.all()
#         if self.request.user.is_authenticated:
#             return queryset
#         return queryset.filter(is_active=True)



@api_view(['GET'])
def user_list(request,email=None):
    if email:
        user = get_user_model().objects.get(email=email)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    users = get_user_model().objects.all()
    users = users.filter(is_active=True)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)