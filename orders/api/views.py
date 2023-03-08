from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser

from orders.models import Order
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
    
    def patch(self, request, *args, **kwargs):
        pass

class MarketOrderListCreateAPIView(ListCreateAPIView):
    pass

class MarketOrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    pass
    
    
    
    
