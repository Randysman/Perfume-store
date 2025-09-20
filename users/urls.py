from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include, reverse_lazy
from django.conf import settings

from .views import profile_view, Register, AsyncPasswordResetView

app_name = 'users'


urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('reset_password/', AsyncPasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('register/', Register.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
]