from django.shortcuts import render, redirect
from .forms import RegisterUser, LoginForm, WorkoutForm
from django.http import HttpResponse
from django.contrib.auth import login as auth_login 
from django.contrib.auth.decorators import login_required
from .models import WorkoutSession
from django.shortcuts import render, get_object_or_404 
# Retrieve an object or return a "404 error" if it doesn't exis.




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

# Login required import used for error prevention. 
@login_required
def display_qr(request):
    return render(request, 'display_qr.html', {'user': request.user})

@login_required
def tracker(request):
    sessions = WorkoutSession.objects.filter(user=request.user).order_by('-date')
    return render(request, 'gymapp/tracker.html', {'sessions': sessions})

@login_required
def add_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            # Tried to set user first but encountered issue. So commit=False used to not save the form,
            # until the user is also set.
            new_session = form.save(commit=False)
            new_session.user = request.user # Sets user to the session data.
            new_session.save()
            return redirect('tracker') # Redirects to tracker page where workout is displayed.
    else:
        form = WorkoutForm()
    return render(request, 'gymapp/add_workout.html', {'form': form})

@login_required
def session_detail(request, session_id):
    session = get_object_or_404(WorkoutSession, pk=session_id)
    return render(request, 'gymapp/session_detail.html', {'session': session})