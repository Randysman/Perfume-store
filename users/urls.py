from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from .views import profile_view, Register

app_name = 'users'


urlpatterns = [
    path('', include('django.contrib.auth.urls')),

    path('register/', Register.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
]