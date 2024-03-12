from django.shortcuts import render

from django.http import HttpResponse

def base(request):
    return render(request,'gymapp/base.html')


def home(request):
    return render(request,'gymapp/home.html')

def notebook(request):
    return render(request,'gymapp/notebook.html')