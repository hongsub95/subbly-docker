from rest_framework.views import APIView 
from rest_framework.response import Response  
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework import status  
from . import serializers

from clothes.models import Clothes,Product
from elasticsearch import Elasticsearch

# for admin
class ClothesReadOrCreateView(generics.ListCreateAPIView):
    queryset = Clothes.objects.prefetch_related('market').prefetch_related('product').prefetch_related('category').all()
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ClothesSerializer
        return serializers.ClothesCreateSerializer

class ClothesRetrieveOrDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        clothes_id = self.kwargs["clothes_pk"]
        return Clothes.objects.filter(clothes=clothes_id)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ClothesSerializer
        return serializers.ClothesPatchSerializer

class ProductReadOrCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
        
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ProductSerializer
        else:
            return serializers.ProductCreateSerializer

#for admin and market master

class SearchApiView(APIView):
    def get(self,request):
        search_keyword = request.query_params.get('search')
        elasticsearch = Elasticsearch("http://192.168.254.16:9200",http_auth=('elastic','elasticpassword'),)
        elastic_sql = f"""
        SELECT id,name,description,price FROM subbly___clothes_clothes_type_2
        WHERE 1=1
        """
        if search_keyword:
            elastic_sql +=f"""
            AND
            (
                MATCH(name_nori, '{search_keyword}')
                OR
                MATCH(description_nori, '{search_keyword}')
                OR
                MATCH(category_name_nori, '{search_keyword}')
                OR
                MATCH(market_name_nori, '{search_keyword}')
                OR
                MATCH(name_chosung, '{search_keyword}')
                OR
                MATCH(description_chosung, '{search_keyword}')
                OR
                MATCH(category_name_chosung, '{search_keyword}')
                OR
                MATCH(market_name_chosung, '{search_keyword}')
                OR
                MATCH(name_jamo, '{search_keyword}')
                OR
                MATCH(description_jamo, '{search_keyword}')
                OR
                MATCH(category_name_jamo, '{search_keyword}')
                OR
                MATCH(market_name_jamo, '{search_keyword}')
            )
            """
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message':'search word param is missing'})
        elastic_sql +=f"""
        ORDER BY score() DESC
        """
        docs = elasticsearch.sql.query(body={"query": elastic_sql})
        if not docs['rows']:
            return Response(data={"message":"찾으시는 상품이 없습니다"})
        prducts = docs['rows']
        
        return Response(prducts)
        