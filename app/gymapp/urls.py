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
    # path('exercise/<int:exercise_id>/set_info/', views.set_info, name='set_info'),
    path('session/<int:session_id>/exercise/<int:exercise_id>/set_info/', views.set_info, name='set_info'),
    path('session/<int:session_id>/exercise/<int:exercise_id>/details/', views.detail_view, name='detail_view'),
    path('delete_sets/', views.delete_sets, name='delete_sets'),
    path('session/<int:session_id>/set/<int:set_id>/edit/', views.edit_set, name='edit_set'),
    # path('exercise/<int:exercise_id>/set/<int:set_id>/edit/', views.edit_set, name='edit_set'),
]