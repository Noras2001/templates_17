from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    """
    Отображает список всех товаров.
    """
    products = Product.objects.all()
    # Передаем список товаров в контекст
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, product_id):
    """
    Отображает детальную информацию о конкретном товаре.
    Если товар не найден, вернется страница 404.
    """
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

