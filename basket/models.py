from django.db import models
from main.models import Product
from users.models import User



class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.name} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price