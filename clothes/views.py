from audioop import reverse
from re import template
from elasticsearch import Elasticsearch
from django.db.models import Prefetch, Case, When
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import DetailView, FormView, ListView,View
from django.contrib.auth.decorators import login_required
import random
from django.db.models import Q 
from clothes.models import Clothes,Product,Categories
from .models import photo as Photo_models
from .forms import SearchForm , ContactForm


def all_clothes(request):
    clothes_set = set()
    clothes = Clothes.objects.all()
    len_clothes = len(clothes)
    if len_clothes <= 10:
        clothes_set.update(clothes)
        return render(
            request,
            "clothes/home.html",
            context={
                "clothes_set": clothes_set,
                "clothes": clothes,
            },
        )
    else:
        num_list = [i for i in range(1,len_clothes+1)]
        num_random = random.sample(num_list,14)
        for i in num_random:
            product = Clothes.objects.get(id=i)
            clothes_set.add(product)
    return render(
        request,
        "clothes/home.html",
        context={
            "clothes_set": clothes_set,
            "clothes": clothes,
        },
    )

def clothes_list(request):
    page = request.GET.get("page", 1)
    clothes_list = Clothes.objects.all()
    paginator = Paginator(clothes_list, 10)
    try:
        clothes = paginator.get_page(page)
        return render(
            request,
            "clothes/clothes_search.html",
            context={"clothes": clothes},
        )
    except EmptyPage:
        return redirect("/")  # home으로 이동

def clothes_list_onepiece(request):
    page = request.GET.get("page", 1)
    category_id = Categories.objects.filter(name="원피스").first().id
    clothes_list = Clothes.objects.filter(category_id = category_id).all()
    
    paginator = Paginator(clothes_list, 10)
    
    try:
        clothes = paginator.get_page(page)
        return render(
            request,
            "clothes/clothes_list.html",
            context={"clothes": clothes},
        )
    except EmptyPage:
        return redirect("/")  # home으로 이동


def clothes_list_upper(request):
    page = request.GET.get("page", 1)
    category_id = Categories.objects.filter(name="상의").first().id
    clothes_list = Clothes.objects.filter(category_id = category_id).all()
    
    paginator = Paginator(clothes_list, 10)
  
    try:
        clothes = paginator.get_page(page)
        return render(
            request,
            "clothes/clothes_list.html",
            context={"clothes": clothes},
        )
    except EmptyPage:
        return redirect("/")  # home으로 이동

def clothes_list_pants(request):
    page = request.GET.get("page", 1)
    category_id = Categories.objects.filter(name="하의").first().id
    clothes_list = Clothes.objects.filter(category_id = category_id).all()
    paginator = Paginator(clothes_list, 10)
    
    try:
        clothes = paginator.get_page(page)
        return render(
            request,
            "clothes/clothes_list.html",
            context={"clothes": clothes},
        )
    except EmptyPage:
        return redirect("/")  # home으로 이동

def clothes_list_shoes(request):
    page = request.GET.get("page", 1)
    category_id = Categories.objects.filter(name="신발").first().id
    clothes_list = Clothes.objects.filter(category_id = category_id).all()
    paginator = Paginator(clothes_list, 10)
    
    try:
        clothes = paginator.get_page(page)
        return render(
            request,
            "clothes/clothes_list.html",
            context={"clothes": clothes},
        )
    except EmptyPage:
        return redirect("/")  # home으로 이동

def clothes_list_outer(request):
    page = request.GET.get("page", 1)

    category_id = Categories.objects.filter(name="신발").first().id
    clothes_list = Clothes.objects.filter(category_id = category_id).all()
    paginator = Paginator(clothes_list, 10)
    
    try:
        clothes = paginator.get_page(page)
        return render(
            request,
            "clothes/clothes_list.html",
            context={"clothes": clothes},
        )
    except EmptyPage:
        return redirect("/")  # home으로 이동




def clothes_detail(request,clothes_id):
    clothes = Clothes.objects.get(pk=clothes_id)
    product = Product.objects.filter(clothes_id=clothes_id).all()
    return render(request,"clothes/clothes_detail.html",{"clothes":clothes,"product":product})
    

def SearchView(request):
    search_keyword = request.GET.get('search_keyword','')
    elasticsearch = Elasticsearch("https://localhost:9200",http_auth=('elastic','elasticpassword'),)
    elastic_sql = f"""
    SELECT id FROM subbly__clothes_clothes_type_2
    WHERE 1 = 1
    """

    if search_keyword:
        elastic_sql +=f"""
        AND(
            MATCH(name_nori, '{search_keyword}')
            OR
            MATCH(description_nori, '{search_keyword}')
            OR
            MATCH(category_name_nori, '{search_keyword}')
            OR
            MATCH(market_name_nori, '{search_keyword}')
        )
        """
    elastic_sql +=f"""
    score() ORDER BY DESC
    """
    response = elasticsearch.sql.query(body={"query":elastic_sql})
    product_ids = [row[0] for row in response['rows']]
    order = Case(*[When(id=id,then=pos) for pos,id in enumerate(product_ids)])
    products = Clothes.objects.filter(id__in=product_ids).prefetch_related('category').prefetch_related('product').prefetch_related('market').order_by(order)
    return render(request,"clothes/search.html",{"products":products})
    
    
class SearchException(Exception):
    pass

                  
            