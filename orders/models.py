from django.db import models
from users.models import User


class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    created = models.DateTimeField(auto_created=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)


    def __str__(self):
        return f'Заказ {self.id}'