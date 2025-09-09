from django.contrib import auth
from django.contrib.auth.views import PasswordResetView
from django.db.models import Prefetch

from orders.models import Order, OrderItem
from shop.services import get_objects_filter
from users.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import views, authenticate, login
from django.views import View


class Register(View):
    template_name='registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main:product_main')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def profile_view(request):
    order = get_objects_filter(Order, user=request.user, status='completed').prefetch_related(Prefetch('items',
    queryset=OrderItem.objects.select_related('product'),)).order_by('-id')
    return render(request, 'registration/profile.html', {'orders': order})

