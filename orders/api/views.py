from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from orders.models import Order
from clothes.models import Product
from .permissions import MarketMasterOrAdminUser
from .serializers import OrderSerializer,OrderCreateSerailizer,OrderPatchSerializer


class AdminOrderListCreateAPIView(ListCreateAPIView):
    queryset = Order.objects.prefetch_related('buyer').prefetch_related('product').prefetch_related('coupon').all()
    permission_classes = [IsAdminUser,]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderSerializer
        else:
            return OrderCreateSerailizer

class AdminOrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdminUser,]
    allowed_methods = ('GET', 'PATCH','DELETE','OPTION')
    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Order.objects.filter(pk=pk).prefetch_related('buyer').prefetch_related('product').prefetch_related('coupon').all()
    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderSerializer
        else:
            return OrderPatchSerializer

    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {"orderstate":"exchange"}
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    
class MarketOrderListCreateAPIView(ListCreateAPIView):
    permission_classes = [MarketMasterOrAdminUser]

    def get_queryset(self):
        market_id = self.kwargs["market_id"]
        return Product.objects.filter(market_id=market_id).prefetch_related('buyer').prefetch_related('coupon').all()
    
    def get_serializer(self, *args, **kwargs):
        if self.request.method == "GET":
            return OrderSerializer
        else:
            return OrderCreateSerailizer

class MarketOrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    pass
    
    
    
    
