from django.shortcuts import render, redirect
from .forms import RegisterUser, LoginForm
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

def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  
        
    else:
        form = LoginForm()

    return render(request, 'gymapp/login.html', {'form':form})