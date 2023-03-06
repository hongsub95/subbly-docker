from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from .forms import OrderForm
from .models import Order
from users.models import User
from clothes.models import Product
from django.contrib import messages
import re 

@login_required
def OrderView(request,pk):
    option= request.POST.get('option')
    if option == None:
        return redirect(reverse('clothes:clothes_detail',kwargs={'clothes_id':pk}))
    else:
        p=re.compile('[0-9]+')
        m=p.search(option)
        n = m.group()  #정규식을 이용하여 Product pk를 구함
        product = Product.objects.get(pk=n)
        return render(request,'orders/order.html',{'product':product})
        
def OrderCompleteView(request):
    pass
    