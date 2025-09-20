from django.contrib import auth
from django.contrib.auth.views import PasswordResetView
from django.db.models import Prefetch

from orders.models import Order, OrderItem
from shop.services import get_objects_filter
from users.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import views, authenticate, login
from django.views import View

from users.tasks import send_email_reset_password


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


class AsyncPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        for user in form.get_users(form.cleaned_data["email"]):
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = defaul_token_generator.make_token(user)

            context = {
                "email": user.email,
                "domain": self.request.get_host(),
                "site_name": "Perfume-store",
                "uid": uid,
                "user": user,
                "token": token,
                "protocol": "https" if self.request.is_secure() else "http",
            }

            subject = "Восстановление пароля"

            message = render_to_string("registration/password_reset_email.html", context)

            send_email_reset_password.delay(
                subject,
                message,
                setting.DEFAULT_FROM_EMAIL,
                [user.email]
            )

        return super().form_valid(form)