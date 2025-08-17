from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Order, OrderItem
from .forms import OrderCreateForm
from basket.models import Basket


def order_create(request):
    basket = Basket(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            order = form.save()
            for item in basket:
                price = item['product'].price()
                OrderItem.objects.create(order=order, product=item['product'], price=price, quantity=item['quantity'])
            basket.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('orders:order_done'))
    else:
        form = OrderCreateForm(request=request)
    return render(request, 'orders/order_create.html', {'form': form, 'baskets': Basket.objects.filter(user=request.user)})