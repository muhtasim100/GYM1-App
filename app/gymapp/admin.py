from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
# Register your models here.
# Editted code from 
# https://stackoverflow.com/questions/70942491/django-add-user-on-admin-page-using-custom-user-model

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        'username', 
        'email', 
        'date_joined', 
        'is_staff', 
        'is_active',
        ] 
    fieldsets = UserAdmin.fieldsets 
    add_fieldsets = UserAdmin.add_fieldsets

admin.site.register(CustomUser, CustomUserAdmin)
