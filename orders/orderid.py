import random
import string
from orders.models import Order

def MakeOrderId():
    order_id = ''
    for _ in range(15):
        order_id+=str(random.randint(0,9))
    order_id = int(order_id)
    try:
        Order.objects.get(order_id=order_id)
    except:
        return order_id
    MakeOrderId()