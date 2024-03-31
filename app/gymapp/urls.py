from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.base, name='base'),
    path('tracker/', views.tracker, name='tracker'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='gymapp/login.html'), name='login'),
    path('login/', views.login, name='login'),


]