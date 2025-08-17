from .models import Basket


def basket_context(request):
    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user)
        total_quantity = sum(basket.quantity for basket in baskets)

    else:
        total_quantity = 0

    return {'basket_quantity': total_quantity}