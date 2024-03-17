from django.shortcuts import render, redirect
from .forms import RegisterUser

from django.http import HttpResponse

def base(request):
    return render(request,'gymapp/base.html')


def home(request):
    return render(request,'gymapp/home.html')

def notebook(request):
    return render(request,'gymapp/notebook.html')

def register(request):
    return render(request,'gymapp/notebook.html')

