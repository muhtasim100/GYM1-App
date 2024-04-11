from django.shortcuts import render, redirect
from .forms import RegisterUser, LoginForm, WorkoutForm, ExerciseForm, DetailsForm, Exercise, ExerciseDetail
from django.db.models import Max
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import login as auth_login 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import WorkoutSession
from django.shortcuts import render, get_object_or_404 
# Retrieve an object or return a "404 error" if it doesn't exis.




def base(request):
    return render(request,'gymapp/base.html')

def home(request):
    return render(request,'gymapp/home.html', {'user': request.user})


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
            last_exercise_order = session.exercises.aggregate(Max('order'))['order__max']
            new_exercise.order = (last_exercise_order or 0) + 1
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
    set_details = exercise.details.all() 
    return render(request, 'gymapp/detail_view.html', {'session': session, 'exercise': exercise,
                                                        'set_details': set_details,})

@login_required
def exercises_done(request, session_id):
    # Retrieve the session by ID and ensure it belongs to the current user.
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

    # Pass existing exercises for this session and the form for adding new exercises to the template.
    exercises = session.exercises.all()
    return render(request, 'gymapp/exercises_done.html', {'session': session, 'exercises': exercises,
                                                           'form': form})

@login_required
def set_info(request, session_id, exercise_id):
    # exercise = get_object_or_404(Exercise, pk=exercise_id, workout_session__user=request.user)
    session = get_object_or_404(WorkoutSession, pk=session_id, user=request.user)
    exercise = get_object_or_404(Exercise, pk=exercise_id, workout_session=session)
    # We order the set numbers and then get the last one which is going to be the highest number.
    # Renamed for clarity - good practice.
    last_set = ExerciseDetail.objects.filter(exercise=exercise).order_by('sets').last()
    # If theres no set_num this means it must be the first set so equate the 'sets' to 1.
    # Or else, add one to the set_num which is the set number of the last set.
    if not last_set:
        set_num = 1
    else:
        set_num = last_set.sets + 1

    if request.method == 'POST':
        form = DetailsForm(request.POST)
        if form.is_valid():
            exercise_detail = form.save(commit=False)
            exercise_detail.exercise = exercise
            exercise_detail.sets = set_num
            exercise_detail.save()
            return redirect('detail_view', session_id=exercise.workout_session_id, exercise_id=exercise_id)
    else:
        form = DetailsForm()

    exercise_details = exercise.details.all()
    return render(request, 'gymapp/set_info.html', 
                  {'exercise': exercise, 
                   'exercise_details': exercise_details, 
                   'form': form,
                   'set_num': set_num,
                   'session_id': exercise.workout_session_id,
    })
# Indent levels are for readability as this is a long line.

@require_POST
@login_required
def delete_sets(request):
    selected_sets = request.POST.getlist('selected_sets')
    if selected_sets:
        # Retrieve an exercise id from the first selected set.
        # Line 153 by ChatGPT to fix error.
        exercise_id = ExerciseDetail.objects.filter(id=selected_sets[0]).values_list('exercise_id', flat=True).first()
        if exercise_id:
            exercise = get_object_or_404(Exercise, pk=exercise_id)
            session_id = exercise.workout_session_id
            # Executes delete.
            ExerciseDetail.objects.filter(id__in=selected_sets).delete()
            # Redirect to detail_view with the defined session_id and exercise_id.
            return redirect('detail_view', session_id=session_id, exercise_id=exercise_id)

@login_required
def edit_set(request, session_id, set_id):
    # Influenced by https://codewithstein.com/how-to-use-the-messages-framework-django-tutorial/
    set_detail = get_object_or_404(ExerciseDetail, pk=set_id, 
                                   exercise__workout_session__id=session_id, exercise__workout_session__user=request.user)
    set_num = set_detail.sets
    # For the display on edit_set.

    if request.method == 'POST':
        form = DetailsForm(request.POST, instance=set_detail)
        if form.is_valid():
            form.save()
            messages.success(request, 'Set updated successfully!') # REMEMBER TO TEST AND CHECK!!
            return redirect('detail_view', session_id=session_id, exercise_id=set_detail.exercise.id)
    else:
        form = DetailsForm(instance=set_detail)

    return render(request, 'gymapp/edit_set.html', {
        'form': form, 
        'set': set_detail, 
        'set_num': set_num, 
        'session_id': session_id,
        'exercise': set_detail.exercise
    })

@login_required
def att_leaderboard(request):
    return render(request,'gymapp/att_leaderboard.html', {'user': request.user})

@require_POST
@login_required
def delete_session(request):
    session_id = request.POST.get('session_id')
    if session_id:
        session = get_object_or_404(WorkoutSession, id=session_id, user=request.user)
        session.delete()
    
@login_required
def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id, workout_session__user=request.user)
    session_id = exercise.workout_session_id  
    exercise.delete()
    return redirect('exercises_done', session_id=session_id)