from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_page(requests):
    '''домашняя страница'''
    return render(requests, 'home.html', {'new_item_text':requests.POST.get('item_text', '')})
