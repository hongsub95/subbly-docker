from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser

from orders.models import Order
from clothes.models import Product
from .permissions import MarketMasterOrAdminUser
from .serializers import OrderSerializer,OrderCreateSerailizer


class AdminOrderListCreateAPIView(ListCreateAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser,]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderSerializer
        else:
            return OrderCreateSerailizer

class AdminOrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser,]
    
    allowed_methods = ('GET', 'PATCH','DELETE','OPTION')
    
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
    
    
    
    
