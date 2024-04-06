from django.shortcuts import render, redirect
from .forms import RegisterUser, LoginForm, WorkoutForm, ExerciseForm, DetailsForm, Exercise
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
def add_exercise(request, session_id):
    session = get_object_or_404(WorkoutSession, pk=session_id, user=request.user)
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            new_exercise = form.save(commit=False)
            new_exercise.workout_session = session
            new_exercise.save()
            return redirect('detail_view', session_id=session.id, exercise_id=new_exercise.id)
    else:
        form = ExerciseForm()
    return render(request, 'gymapp/add_exercise.html', {'form': form, 'session': session})

@login_required
def detail_view(request, session_id, exercise_id):
    # Gets the specific workout session clicked on by the user and the specific exercise.
    session = get_object_or_404(WorkoutSession, pk=session_id, user=request.user)
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    return render(request, 'gymapp/detail_view.html', {'session': session, 'exercise': exercise})

@login_required
def exercises_done(request, session_id):
    # Retrieve the session by ID and ensure it belongs to the current user
    session = get_object_or_404(WorkoutSession, pk=session_id, user=request.user)
    
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            new_exercise = form.save(commit=False)
            new_exercise.workout_session = session
            new_exercise.save()
            return redirect('exercises_done', session_id=session_id)
    else:
        form = ExerciseForm()

    # Pass existing exercises for this session and the form for adding new exercises to the template
    exercises = session.exercises.all()
    return render(request, 'gymapp/exercises_done.html', {'session': session, 'exercises': exercises, 'form': form})

@login_required
def set_info(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id, workout_session__user=request.user)
    if request.method == 'POST':
        form = DetailsForm(request.POST)
        if form.is_valid():
            exercise_detail = form.save(commit=False)
            exercise_detail.exercise = exercise
            exercise_detail.save()
            return redirect('detail_view', session_id=exercise.workout_session_id, exercise_id=exercise_id)
    else:
        form = DetailsForm()

    exercise_details = exercise.details.all()
    return render(request, 'gymapp/set_info.html', {'exercise': exercise, 'exercise_details': exercise_details, 'form': form})
