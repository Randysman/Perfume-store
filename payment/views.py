from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from yookassa import Configuration
from orders.models import Order
from django.conf import settings
from main.models import Product


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, order_id)

    if Order.objects.filter(user=request.user, order=order, status='completed').exists():
        messages.info(request, f'Вы приобрели заказ {order_id}')
        return redirect('main:product_main')




