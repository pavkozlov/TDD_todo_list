from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item


# Create your views here.
def home_page(requests):
    '''домашняя страница'''
    if requests.method == 'POST':
        Item.objects.create(text=requests.POST['item_text'])
        return redirect('/')
    items = Item.objects.all()
    return render(requests, 'home.html', {'items': items})
