from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.base, name='base'),
    path('tracker/', views.tracker, name='tracker'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('add_workout/', views.add_workout, name='add_workout'),
    path('session/<int:session_id>/', views.add_exercise, name='add_exercise'),
    path('session/<int:session_id>/exercises/', views.exercises_done, name='exercises_done'),
    path('session/<int:session_id>/exercise/<int:exercise_id>/set_info/', views.set_info, name='set_info'),
    path('session/<int:session_id>/exercise/<int:exercise_id>/details/', views.detail_view, name='detail_view'),
    path('delete_sets/', views.delete_sets, name='delete_sets'),
    path('session/<int:session_id>/set/<int:set_id>/edit/', views.edit_set, name='edit_set'),
    path('att_leaderboard/', views.att_leaderboard, name='att_leaderboard'),
    path('delete_session/', views.delete_session, name='delete_session'),
    path('exercise/delete/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('bench_leaderboard/', views.bench_leaderboard, name='bench_leaderboard'),
    path('squat_leaderboard/', views.squat_leaderboard, name='squat_leaderboard'),
    path('dead_leaderboard/', views.dead_leaderboard, name='dead_leaderboard'),
    path('forum/', views.forum, name='forum'),


]