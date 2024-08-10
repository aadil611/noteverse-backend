from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self,data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("passwords must match")
        return data
    
    def create(self, validated_data):
        data = validated_data.copy()
        
        data['password'] = validated_data['password1']
        data.pop('password1')
        data.pop('password2')
        
        return get_user_model().objects.create_user(**data)
    
    
    class Meta:
        model = get_user_model()
        fields = ['email','password1','password2']
        extra_kwargs = {'password': {'write_only': True}}
        
        
class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['email'] = user.email
        return token