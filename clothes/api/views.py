from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from . import serializers
from .permissions import IsOwnerOrAdmin
from clothes import models


class ClothesReadOrCreateView(generics.ListCreateAPIView):
    queryset = models.Clothes
    permission_classes = []
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ClothesSerializer
        return serializers.ClothesCreateSerializer

class ClothesRetrieveOrDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ClothesSerializer
        return serializers.ClothesPatchSerializer

