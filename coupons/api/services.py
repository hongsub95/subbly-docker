import random
import string
from coupons.models import Coupon

def MakeCouponNum():
    coupon_num = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    try:
        Coupon.objects.get(coupon_id=coupon_num)
    except:
        return coupon_num
    MakeCouponNum()