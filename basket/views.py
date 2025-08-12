from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from main.models import Product
from .models import Basket


@login_required
def basket_view(request):
    user = request.user
    baskets = Basket.objects.filter(user=user)
    total_quantity = 0
    total_sum = 0
    for basket in baskets:
        total_quantity += basket.quantity
        total_sum += basket.sum()

    return render(request, 'basket/basket.html', {'sum': total_sum, 'quantity': total_quantity, 'baskets': Basket.objects.filter(user=request.user)})



def basket_add(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
        return HttpResponseRedirect(current_page)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(current_page)