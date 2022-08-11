from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from users import models as users_models
from .serializers import UserSerializer,UserTokenObtainSerializer


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
    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        refresh = serializer.validated_data['refresh']



