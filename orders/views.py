from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from shop.services import get_objects_filter
from .models import Order, OrderItem
from .forms import OrderCreateForm
from basket.models import Basket
import logging


logger = logging.getLogger(__name__)


def order_create(request, create_yookassa_payment=None):
    if request.user.is_authenticated:
        baskets = get_objects_filter(Basket, user=request.user)
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
                OrderItem.objects.create(order=order, product=item.product, price=price, quantity=item.quantity)
            baskets.delete()
            return redirect('payment:checkout', order_id=order.id)
    else:
        form = OrderCreateForm(request=request)
    return render(request, 'orders/order_create.html', {'form': form, 'baskets': Basket.objects.filter(user=request.user)})
