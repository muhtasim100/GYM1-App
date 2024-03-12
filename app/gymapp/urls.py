from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('notebook/', views.notebook, name='notebook'),
    path('home/', views.home, name='home'),
    
]