from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings


def index(request):
    return render(request,'index.html')

def index2(request):
    return render(request,'index2.html')

def index3(request):
    return render(request,'index3.html')

def index4(request):
    return render(request,'index4.html')

def index5(request):
    return render(request,'index5.html')

def index6(request):
    return render(request,'index6.html')