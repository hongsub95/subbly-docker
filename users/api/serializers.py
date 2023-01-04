from lib2to3.pgen2 import token
from logging import _STYLES
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
        
        return token

class ApiRefreshRefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    pass

class RegisterSerializer(serializers.Serializer):
    class Meta:
        model = users_models.User
        fields = '__all__'
    def create(self,validated_data):
        username = validated_data.get("email")
        password = validated_data.get("password")
        gender = validated_data.get("gender")
        birthday = validated_data.get("validated_data")
        is_staff=validated_data.get("is_staff")
        user = users_models.User(email=username,gender=gender,birthday=birthday,is_staff=is_staff)
        user.set_password(password)
        user.save()
        return user

