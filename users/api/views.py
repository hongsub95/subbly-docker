from requests import Response
from rest_framework import viewsets
from users import models as users_models
from .serializers import UserSerializer

class UserViewset(viewsets.ModelViewSet):
    queryset = users_models.User.objects.all()
    serializer_class = UserSerializer