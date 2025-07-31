
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Category, Product


class Product(ListView):
    model = Product
    queryset = Product.objects.all()
    template_name = "main/product/list.html"