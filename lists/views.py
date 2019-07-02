from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List


# Create your views here.
def home_page(requests):
    '''домашняя страница'''
    return render(requests, 'home.html')


def view_list(requests, list_id):
    '''просмотреть список'''
    list_ = List.objects.get(id=list_id)
    return render(requests, 'list.html', {'list': list_})


def new_list(requests):
    '''новый список'''
    list_ = List.objects.create()
    Item.objects.create(text=requests.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')

def add_item(requests, list_id):
    '''новый элемент'''
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=requests.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')