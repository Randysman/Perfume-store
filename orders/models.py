from django.db import models

from main.models import Product
from users.models import User


class Order(models.Model):
    STATUS_CHOICES = (
    ('pending', 'В ожидании'),
    ('processing', 'В обработке'),
    ('completed', 'Завершен'),
    ('cancelled', 'Отменен'),
    )

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(default='pending', max_length=20, choices=STATUS_CHOICES)
    yookassa_payment_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity