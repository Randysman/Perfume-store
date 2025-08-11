from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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

    return render(request, 'basket/basket.html', {'sum': total_sum, 'quantity': total_quantity})