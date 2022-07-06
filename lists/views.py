from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from clothes import models as clothes_models
from . import models


def _list_id(request):
    list = request.session.session_key
    if not list:
        list = request.session.create()
    return list


def add_list(request, clothes_pk):
    clothes = clothes_models.Clothes.objects.get(pk=clothes_pk)
    try:
        list = models.List.objects.get(list_id=_list_id(request))
    except models.List.DoesNotExist:
        list = models.List.objects.create(list_id=_list_id(request))
        list.save()
    try:
        list_item = models.ListItem.objects.get(clothes=clothes, list=list)
        list_item.quantity += 1
        list_item.save()
    except models.ListItem.DoesNotExist:
        list_item = models.ListItem.objects.create(
            clothes=clothes, quantity=1, list=list
        )
        list_item.save()
    return redirect("lists:list_detail")


def list_detail(request):
    total = 0
    cnt = 0
    list_items = None
    try:
        list = models.List.objects.get(list_id=_list_id(request))
        list_items = models.ListItem.objects.filter(list=list, active=True)
        for item in list_items:
            total += item.clothes.price * item.quantity
            cnt += item.quantity
    except ObjectDoesNotExist:
        pass
    return render(
        request,
        "lists/list_detail.html",
        {"list_items": list_items, "total": total, "cnt": cnt},
    )


def list_delete(request, clothes_pk):
    list = models.List.objects.get(list_id=_list_id(request))
    clothes = get_object_or_404(clothes_models.Clothes, pk=clothes_pk)
    list_item = models.ListItem.objects.get(clothes=clothes, list=list)
    if list_item.quantity > 1:
        list_item.quantity -= 1
        list_item.save()
    else:
        list_item.delete()
    return redirect("lists:list_detail")
