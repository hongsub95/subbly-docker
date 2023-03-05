from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from .forms import OrderForm
from .models import Order
from users.models import User
from clothes.models import Product

import re 

@login_required
def OrderView(request):
    option= request.POST.get('option')
    p=re.compile('[0-9]+')
    m=p.search(option)
    n = m.group()
    product = Product.objects.get(pk=n)
    print(product.size,product.colors)
    return render(request,'orders/order.html',{'product':product})
    
    