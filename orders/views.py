from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
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
        print(request.POST,request.GET)
        return render(request,'orders/order.html',{'product':product,"order":Order})
        

@login_required
def OrderCompleteView(request,pk):
    product = Product.objects.get(pk=pk)
    cate = request.POST.get('paycate')
    address_kakao = request.POST.get('address')
    address_detail = request.POST.get('address_detail')
    Order.objects.create(buyer=request.user,product=product,address=address_kakao + address_detail,paycate=cate)
    return render(request,'orders/complete.html')
        
        
        

    