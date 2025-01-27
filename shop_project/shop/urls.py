from django.urls import path
from .views import product_list, product_detail

urlpatterns = [
    path('', product_list, name='product_list'),  # главная страница со списком товаров
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]
