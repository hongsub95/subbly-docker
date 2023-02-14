from django.urls import path
from coupons.api import views

app_name ='coupons_api'

urlpatterns = [
    path('',views.AdminCouponListCreateAPIView.as_view(),name="Coupon-List-Create"),
    path('<int:coupon_pk>/',views.AdminCouponRetrieveAPIView.as_view(),name="Coupon-Retrieve"),
    path('issuance/<int:user_pk>/<int:coupon_pk>/',views.AdminCouponIssuanceAPIView.as_view(),name="Coupon-Issuance"),
    path('discount/<str:coupon_id>/',views.CouponUseAPIView.as_view(),name="Coupon-use"),  # 엔드포인트 뭘로 작명해야할지 딱히 떠오르지가 않음....
    path('deletion/<int:pk>/',views.AdminCouponDeleteAPIView.as_view(),name="Coupon-delete"), #엔드포인트 뭘로 작명해야할지 딱히 떠오르지가 않음2....
    
]