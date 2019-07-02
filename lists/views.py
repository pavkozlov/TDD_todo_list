from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item


# Create your views here.
def home_page(requests):
    '''домашняя страница'''
    return render(requests, 'home.html')


def view_list(requests):
    '''просмотреть список'''
    items = Item.objects.all()
    return render(requests, 'list.html', {'items': items})


def new_list(requests):
    '''новый список'''
    Item.objects.create(text=requests.POST['item_text'])
    return redirect('/lists/first_list_on_the_world/')
