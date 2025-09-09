from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

from shop.services import get_objects_all
from .models import Category, Product


class ProductView(ListView):
    model = Product
    template_name = "main/index/index.html"
    context_object_name = "products"


class ProductListView(ListView):
    model = Category
    template_name = "main/product/list.html"


    def get(self, request, category_slug=None):
        page = request.GET.get('page', 1)
        category = None
        products = get_objects_all(Product)
        categories = get_objects_all(Category)
        paginator = Paginator(products, 6)
        current_page = paginator.page(int(page))
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            paginator = Paginator(products.filter(category=category), 6)
            current_page = paginator.page(int(page))
        return render(request, 'main/product/list.html',
                      {'category': category, 'products': current_page, 'categories': categories, 'slug': category_slug})


class ProductDetailView(DetailView):
    model = Product
    template_name = "main/product/detail.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "products"