from rest_framework.views import APIView 
from rest_framework.response import Response  
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status  
from . import serializers

from clothes.models import Clothes
from elasticsearch import Elasticsearch


class ClothesReadOrCreateView(generics.ListCreateAPIView):
    queryset = Clothes.objects.prefetch_related('market').prefetch_related('product').prefetch_related('category').all()
    permission_classes = []
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ClothesSerializer
        return serializers.ClothesCreateSerializer

class ClothesRetrieveOrDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    queryset = Clothes
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ClothesSerializer
        return serializers.ClothesPatchSerializer

class SearchApiView(APIView):
    def get(self,request):
        search_keyword = request.query_params.get('search')
        elasticsearch = Elasticsearch("http://192.168.254.16:9200",http_auth=('elastic','elasticpassword'),)
        if not search_keyword:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"찾으시는 상품이 없습니다."})
        docs = elasticsearch.search(index='subbly___clothes_clothes_type_2___v2')
        data_list = docs['hits']['hits']
        return Response(data_list)
        