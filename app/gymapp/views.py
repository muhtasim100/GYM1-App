from django.shortcuts import render, redirect
from .forms import RegisterUser, LoginForm
from django.http import HttpResponse
from django.contrib.auth import login as auth_login 
from django.contrib.auth.decorators import login_required
from .models import WorkoutSession


def base(request):
    return render(request,'gymapp/base.html')

def home(request):
    return render(request,'gymapp/home.html', {'user': request.user})

# def tracker(request):
#     return render(request,'gymapp/tracker.html')

def register(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)

        if form.is_valid(): # Erorr prevention.
            form.save()
            return redirect('login')  # Redirect to home for now.
    else:
        form = RegisterUser()
    return render(request, 'gymapp/register.html', {'form':form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  
    else:
        form = LoginForm()
    return render(request, 'gymapp/login.html', {'form':form})

@login_required
def display_qr(request):
    return render(request, 'display_qr.html', {'user': request.user})


@login_required
def tracker(request):
    sessions = WorkoutSession.objects.filter(user=request.user).order_by('-date')
    return render(request, 'gymapp/tracker.html', {'sessions': sessions})

