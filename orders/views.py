from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Order, OrderItem
from .forms import OrderCreateForm
from basket.models import Basket
import logging


logger = logging.getLogger(__name__)


def order_create(request, create_yookassa_payment=None):
    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user)
    else:
        baskets = []

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in baskets:
                price = item.product.price
                OrderItem.objects.create(product=item.product, price=price, quantity=item.quantity, user=request.user)
                payment = create_yookassa_payment(order, request, item)
            baskets.delete()
            return render(request, 'orders/order_done.html', {'order': order})
        else:
            form = OrderCreateForm(request=request)
        return render(request, 'orders/order_create.html', {'form': form, 'baskets': Basket.objects.filter(user=request.user)})