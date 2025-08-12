from django.urls import path
from .views import *


app_name = 'basket'

urlpatterns = [
    path('', basket_view, name='basket'),
    path('basket_add/<int:product_id>/', basket_add, name='basket_add'),
]