from django.urls import path

from .views import *

app_name = 'main'


urlpatterns = [
    path('', Product.as_view(),name='product_list'),

]