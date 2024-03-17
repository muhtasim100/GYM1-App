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
    if request.method == 'POST':
        form = RegisterUser(request.POST)

        if form.is_valid(): # Erorr prevention.
            form.save()
            return redirect('home')  # Redirect to home for now.
        # Note: make sign in page.

    else:
        form = RegisterUser()

    return render(request, 'gymapp/register.html', {'form':form})

