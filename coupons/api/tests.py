from django.urls import reverse
from requests.auth import HTTPBasicAuth
from rest_framework.test import APITestCase,APIClient,APIRequestFactory,force_authenticate
from coupons.api.views import AdminCouponListCreateAPIView
from coupons.models import Coupon
from users.models import User
from coupons.api.services import MakeCouponNum


class TestCoupon(APITestCase):
    
    COUPON_ID = MakeCouponNum()
    NAME = "설날특별쿠폰"
    NAME2 = "추석특별쿠폰"
    DESCRIPTION = "설날특별할인쿠폰"
    DESCRIPTION2 = "추석특별할인쿠폰"
    MIN_PRICE = 30000
    DISCOUNT_1 = 5000
    DISCOUNT_2 = 50
    COUPON_CATE_1=Coupon.CouponChoice.flat_rate
    COUPON_CATE_2=Coupon.CouponChoice.fixed_rate
    def setUp(self) -> None:
        admin = User.objects.create(username="admin@admin.com", name="관리자",is_staff=True,gender=User.GenderChoices.FEMALE)
        admin.set_password("admin")
        admin.save()
        self.admin =admin
        Coupon.objects.create(name=self.NAME,coupon_id=self.COUPON_ID,description=self.DESCRIPTION,min_price=self.MIN_PRICE,discount=self.DISCOUNT_1,coupon_cate=self.COUPON_CATE_1)
    
    def test_get_coupon_without_admin(self):
        factory = APIRequestFactory()
        view = AdminCouponListCreateAPIView.as_view()
        request = factory.get('/coupon_api/')
        response = view(request)
        
        self.assertEqual(response.status_code,403)
    
    def test_get_coupon(self):
        factory = APIRequestFactory()
        admin = self.admin
        view = AdminCouponListCreateAPIView.as_view()
        request = factory.get('/coupon_api/')
        force_authenticate(request,user=admin)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),4)
        print(response.json)
    
    
    def test_create_coupons(self):
        factory = APIRequestFactory()
        admin = self.admin
        view = AdminCouponListCreateAPIView.as_view()
        coupon_id = MakeCouponNum()
        request = factory.post(reverse('coupon_url:Coupon-List-Create'),{"coupon_id":coupon_id,"name":self.NAME2,"description":self.DESCRIPTION2,"min_price":self.MIN_PRICE,"discount":self.DISCOUNT_2,"coupon_cate":self.COUPON_CATE_2})
        force_authenticate(request,user=admin)
        response = view(request)
        self.assertEqual(
            response.status_code,201
        )
        
        
    
        