from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Order, OrderItem
from .forms import OrderCreateForm
from basket.models import Basket


def order_create(request):
    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user)
    else:
        baskets = []

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            order = form.save()
            order.user = request.user
            order.save()
            for item in baskets:
                price = item.product.price
                OrderItem.objects.create(order=order, product=item.product, price=price, quantity=item.quantity)
            baskets.delete()
            return render(request, 'orders/order_done.html', {'order': order})
    else:
        form = OrderCreateForm(request=request)
    return render(request, 'orders/order_create.html', {'form': form, 'baskets': Basket.objects.filter(user=request.user)})