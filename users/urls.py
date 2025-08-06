from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from .views import profile_view

app_name = 'users'


urlpatterns = [
    path('', include('django.contrib.auth.urls')),

]