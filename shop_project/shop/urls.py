# shop/urls.py
from django.urls import path
from .views import product_list, product_detail, ajax_product_list

urlpatterns = [
    path('', product_list, name='product_list'),  # главная страница со списком товаров
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('ajax-product-list/', ajax_product_list, name='ajax_product_list'),
]




