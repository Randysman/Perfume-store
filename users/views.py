from django.shortcuts import render
from django.contrib.auth import views


def profile_view(request):
    return render(request, 'profile.html')