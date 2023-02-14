from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view,permission_classes
from rest_framework.generics import ListCreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from coupons.api.paginations import LargeResultsSetPagination
from coupons.api.serializers import CouponSerializer,CouponCreateSerializer,CouponPatchSerializer
from coupons.models import Coupon
from users.models import User


class AdminCouponListCreateAPIView(ListCreateAPIView):
    queryset = Coupon.objects.all()
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CouponSerializer
        else:
            return CouponCreateSerializer

class AdminCouponRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CouponSerializer
    
    def get_queryset(self):
        coupon_pk = self.kwargs["coupon_pk"]
        coupon = Coupon.objects.filter(pk=coupon_pk)
        return coupon

#쿠폰 발급
class AdminCouponIssuanceAPIView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CouponPatchSerializer
    allowed_methods = ('GET', 'PATCH', 'OPTION')
    
    def get_queryset(self):
        coupon_pk = self.kwargs["coupon_pk"]
        coupon = Coupon.objects.filter(pk=coupon_pk)
        return coupon
    
    def patch(self, request, *args, **kwargs):
        user_pk = kwargs.pop("user_pk")
        try:
            user = User.objects.get(pk=user_pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"존재하지 않은 유저입니다."})
        instance = self.get_object()
        # 이미 발급된 쿠폰
        if instance.is_issued:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"이미 발급된 쿠폰입니다"})
        # 사용하지 않은쿠폰 개수 10개 이상 
        elif user.coupon.filter(is_used=False).count() >= 10 :
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":f"{user.name}님의 사용하지 않은 쿠폰의 개수가 10개 이상입니다."})
        data = {"is_issued":True,"owner":user_pk}
        serializer = self.get_serializer(instance,data=data,partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

#쿠폰 사용
class CouponUseAPIView(UpdateAPIView):
    serializer_class = CouponSerializer
    allowed_methods = ('GET','PATCH','OPTION')
    lookup_field = "coupon_id"
    queryset = Coupon
    def get_queryset(self):
        coupon_id = self.kwargs["coupon_id"]
        coupon = Coupon.objects.filter(coupon_id=str(coupon_id))
        return coupon
    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # 사용된 쿠폰 일 경우
            if instance.is_used:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"이미 사용한 쿠폰입니다."})
            # 발급되지 않은 쿠폰 일 경우
            elif instance.is_issued is False:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"발급 된 쿠폰이 아닙니다"})
            else:
                data = {"is_used":True}
                serializer = self.get_serializer(instance, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"존재하지 않은 쿠폰 번호 입니다."})

#soft delete로 페이지에 나타나진 않지만 db에는 기록되어 있음
class AdminCouponDeleteAPIView(DestroyAPIView):
    serializer_class = CouponPatchSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        pk = self.kwargs["pk"]
        coupon = Coupon.objects.filter(pk=pk)
        return coupon
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_issued:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"발급 된 쿠폰은 삭제 하실 수 없습니다."})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,data={"message":"삭제완료^^"})


    

        
    
