from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from yookassa import Configuration, Payment
from orders.models import Order
from django.conf import settings
from main.models import Product
from uuid import uuid4
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


logger = logging.getLogger(__name__)


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, order_id)

    if Order.objects.filter(user=request.user, order=order, status='completed').exists():
        messages.info(request, f'Вы приобрели заказ {order_id}')
        return redirect('main:product_main')


def create_yookassa_payment(request, order, item):
    receipt_items = [{
        "description" : f"Заказ: {order.id}",
        "quantity" : item.quantity,
        "amount": {
            "value": f"{order.price}",
            "currency": "RUB"
        },
        "vat_code": getattr(settings, 'YOOKASSA_VAT_CODE', 1),
        "payment_mode": "full_payment",
        "payment_subject": "commodity"
    }]

    customer = {
        "email": order.email
    }

    try:
        idempotence_key = str(uuid4())
        payment = Payment.create({
            "value": f"{order.price}",
            "currency": "RUB"
        },
            {"confirmation": {
            "type" : "redirect",
            "return_url": request.build_absolute_url('/orders/yookassa/success/' + f'?order_id={order.id}')
        },
            "capture": True,
            "description": f"Заказ#{order.id}",
            "metadata": {
                "order_id": order.id,
                "user_id": order.user.id
            },
            "receipt": {
                "customer": customer,
                "items": receipt_items
            }
            }, idempotence_key)

        order.yookassa_payment_id = payment.id
        order.save()
        return payment
    except Exception as e:
        logger.error(f"Ошибка создания платежа ЮКасса: {str(e)}")
        raise


def yookassa_cancel(request):
    order_id = request.GET.get('order_id')
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        order.status = 'cancelled'
        order.save()
        messages.error(request, 'Платеж отменен.')
        return render(request, 'payment/yookassa_cancel.html', {'order': order})
    return redirect('orders:checkout')


def yookassa_success(request):
    order_id = request.GET.get('order_id')
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        if order.status == 'completed':
            messages.success(request, 'Оплата прошла успешно.')
            return render(request, 'payment/yookassa_success.html', {'order': order})
        elif order.status == 'cancelled':
            return redirect('payment:yookassa_cancel')
        if order.yookassa_payment_id:
            try:
                payment = Payment.find_one(order.yookassa_payment_id)
                if payment.status == 'succeeded':
                    order.status = 'completed'
                    order.save()
                    messages.success(request, 'Оплата прошла успешно!')
                    return render(request, 'payment/yookassa_success.html', {'order': order})
                elif payment.status in ['canceled', 'failed']:
                    order.status = 'cancelled'
                    order.save()
                    return redirect('payment:yookassa_cancel')
            except Exception as e:
                logger.error(f'Ошибка проверки платежа: {str(e)}')
        return render(request, 'payment/yookassa_pending.html', {'order': order})
    return redirect('main:product_main')