
# shop/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
import datetime

from .models import Product


def product_list(request):
    """
    Обычное представление для fallback, 
    если у пользователя отключён JavaScript.
    Также учитывает сортировку (и фильтры при желании).
    """
    from django.core.paginator import Paginator

    # Считываем те же GET-параметры, что и в ajax_product_list
    sort_by = request.GET.get('sort_by', '-quantity_sold')
    page_number = request.GET.get('page', '1')

    qs = Product.objects.all()

    # Можно продублировать фильтры, если хотите,
    # чтобы и без AJAX фильтрация работала:
    category = request.GET.get('category', '').strip()
    if category:
        qs = qs.filter(category=category)

    min_price = request.GET.get('min_price', '').strip()
    if min_price:
        try:
            qs = qs.filter(price__gte=float(min_price))
        except ValueError:
            pass

    max_price = request.GET.get('max_price', '').strip()
    if max_price:
        try:
            qs = qs.filter(price__lte=float(max_price))
        except ValueError:
            pass

    
    date_range = request.GET.get('date_range', '').strip()
    if date_range:
        try:
            days = int(date_range)
            from_date = timezone.now() - datetime.timedelta(days=days)
            qs = qs.filter(created_at__gte=from_date)
        except ValueError:
            pass

    # Применяем сортировку
    if sort_by:
        qs = qs.order_by(sort_by)

    # Пагинация
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,  # товары на текущей странице
        'page_obj': page_obj,  # для шаблона
    }
    return render(request, 'shop/product_list.html', context)

    

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})


def ajax_product_list(request):
    """
    Представление для AJAX. То же самое, только возвращает JSON вместо HTML.
    """
    qs = Product.objects.all()

    # Фильтрация
    category = request.GET.get('category', '').strip()
    if category:
        qs = qs.filter(category=category)

    min_price = request.GET.get('min_price', '').strip()
    if min_price:
        try:
            qs = qs.filter(price__gte=float(min_price))
        except ValueError:
            pass

    max_price = request.GET.get('max_price', '').strip()
    if max_price:
        try:
            qs = qs.filter(price__lte=float(max_price))
        except ValueError:
            pass

    date_range = request.GET.get('date_range', '').strip()
    if date_range:
        try:
            days = int(date_range)
            from_date = timezone.now() - datetime.timedelta(days=days)
            qs = qs.filter(created_at__gte=from_date)
        except ValueError:
            pass

    # Сортировка
    sort_by = request.GET.get('sort_by', '-quantity_sold')
    if sort_by:
        qs = qs.order_by(sort_by)

    # Пагинация
    page_number = request.GET.get('page', '1')
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page_number)

    # Сбор данных для JSON
    products_data = []
    for product in page_obj:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'category': product.category,
            'category_display': product.get_category_display(),
            'quantity_sold': product.quantity_sold,
            'availability_status': product.get_availability_status(),
        })

    data = {
        'products': products_data,
        'page': page_obj.number,
        'num_pages': paginator.num_pages,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
    }
    return JsonResponse(data)
