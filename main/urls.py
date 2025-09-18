from django.urls import path

from .views import *

app_name = 'main'


urlpatterns = [
    path('', ProductView.as_view(), name='product_main'),
    path('header/', header_view, name='header'),
    path('shop/', ProductListView.as_view(), name='product_list'),
    path('shop/category/<slug:category_slug>', ProductListView.as_view(), name='product_list_by_category'),
    path('shop/<slug:post_slug>/', ProductDetailView.as_view(), name='product_detail')
]