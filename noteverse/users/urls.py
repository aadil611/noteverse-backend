from django.contrib import admin
from django.urls import path,include

from .views import SignUpView, user_list
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('users/<str:email>/', user_list, name='user-retrieve'),
    path('users/', user_list, name='user-list'),
]
