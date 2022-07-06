from re import template
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import DetailView, FormView
import random
from django.db.models import Q 
from . import models as clothes_models
from .forms import SearchForm , ContactForm

def contact_view(request):
    form = ContactForm()
    context = {'form': form}
    template_name = 'clothes/index.html'
    return render(request, template_name, context)

def all_clothes(request):
    clothes_set = set()
    clothes = clothes_models.Clothes.objects.all()
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
    clothes_list = clothes_models.Clothes.objects.all()
    paginator = Paginator(clothes_list, 10)
    clothes_category = clothes_models.Clothes.objects.get("Category")
    
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
    model = clothes_models.Clothes


class SearchView(FormView):
    template_name = "clothes/search.html"
    form_class = SearchForm
    
    def form_valid(self,form):
        name = form.cleaned_data.get("name")
        clothes_list = clothes_models.Clothes.objects.filter(Q(name__icontains=name) | Q(description__icontains=name)).distinct()
        return render(self.request,self.template_name,{'form':form,'clothes_list':clothes_list,'name':name})
                  
            