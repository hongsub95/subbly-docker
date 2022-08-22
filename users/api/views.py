from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from users import models as users_models
from .serializers import UserSerializer,UserTokenObtainSerializer,ApiRefreshRefreshTokenSerializer


class UserViewset(viewsets.ViewSet):
    def list(self,request):
        queryset = users_models.User.objects.all()
        serialize = UserSerializer(queryset,many=True)
        return Response(serialize.data)

class UserTokenView(TokenObtainPairView):
    serializer_class = UserTokenObtainSerializer

class UserRefreshTokenView(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = ApiRefreshRefreshTokenSerializer
    
    def post(self, request: HttpRequest):
        serializer: ApiRefreshRefreshTokenSerializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        refresh: str = serializer.validated_data['refresh']

        try:
            refresh_token: RefreshToken = RefreshToken(refresh)
        except TokenError as e:
            raise InvalidToken(e)

        user: users_models.User = get_object_or_404(users_models.User, id=refresh_token['user_id'])
        new_refresh_token = UserTokenObtainSerializer.get_token(user)  
        new_access_token = new_refresh_token.access_token
        refresh_token.blacklist()  

        return Response({
            'refresh': str(new_refresh_token),
            'access': str(new_access_token),
        })



