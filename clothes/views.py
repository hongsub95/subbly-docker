from audioop import reverse
from re import template
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import DetailView, FormView, ListView,View
import random
from django.db.models import Q 
from .models import Clothes as clothes_models
from .models import photo as Photo_models
from .forms import SearchForm , ContactForm


def all_clothes(request):
    clothes_set = set()
    clothes = clothes_models.objects.all()
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
        for _ in range(10):
            num = random.randint(0, len_clothes - 1)
            clothes_set.add(clothes[num])
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
    clothes_list = clothes_models.objects.all()
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
    clothes_list = clothes_models.objects.filter(category_id=1)
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
    clothes_list = clothes_models.objects.filter(category_id=2)
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
    clothes_list = clothes_models.objects.filter(category_id=3)
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
    clothes_list = clothes_models.objects.filter(category_id=4)
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
    clothes_list = clothes_models.objects.filter(category_id=5)
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




class clothes_detail(DetailView):
    model = clothes_models


class SearchView(View):

    def get(self,request):

        query = request.GET.get('search')

        try:
            clothes_list = clothes_models.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) ).distinct()
            paginator = Paginator(clothes_list,10,orphans=5)
            page = request.GET.get("page",1)
            clothes = paginator.get_page(page)
            return render(request, 'clothes/search.html', {'query': query, 'clothes': clothes})
        except ValueError:
            return redirect('/')

class SearchException(Exception):
    pass

                  
            