from django.http import HttpResponse
from django.shortcuts import render
from .models import Choice

choice = Choice()

def index(request):
    return render(request,'show_up/index.html')


def price(request):
    return render(request,'show_up/price.html')

def genre(request):
    if request.method == 'POST':
        #int값 외 다른값 들어올 시 처리 해야함
        choice.price = int(request.POST['price'])
        print(request.POST)
        choice.save()

    return render(request,'show_up/genre.html')

def runtime(request):
    if request.method == 'POST':
        choice.genre = request.POST['genre']

    return render(request,'show_up/runtime.html')

def day(request):
    if request.method == 'POST':
        choice.runtime = request.POST['runtime']

    return render(request,'show_up/day.html')

def age(request):
    if request.method == 'POST':
        choice.day = request.POST['day']

    return render(request,'show_up/age.html')

def result(request):
    if request.method == 'POST':
        choice.age = request.POST['age']
        
    return render(request,'show_up/result.html',{'choice':choice})
