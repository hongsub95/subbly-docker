from lib2to3.pgen2 import token
from users import models as users_models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_models.User
        exclude = ()
        read_only_fields = ["pk","created"]

class UserTokenObtainSerializer(TokenObtainPairSerializer): #token 페어로드
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token['email'] = user.email
        token['gender'] = user.gender
        token['birthday'] = user.birthday
        token['is_staff'] = user.is_staff
        token['is_active'] = user.is_active
        
        return token

class ApiRefreshRefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    pass
    

