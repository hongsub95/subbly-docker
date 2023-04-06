import random
import string
from orders.models import Order

def MakeOrderId():
    order_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(15))
    try:
        Order.objects.get(order_id=order_id)
    except:
        return order_id
    MakeOrderId()