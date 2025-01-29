
# shop/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
import datetime

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



def ajax_product_list(request):
    """
    Представление для обработки AJAX-запросов (GET-параметров) 
    и возврата JSON-данных о товарах с учётом фильтрации, 
    сортировки и пагинации.

    Параметры:
    - category: строка (значение поля category, например 'bouquet')
    - min_price: число (минимальная цена)
    - max_price: число (максимальная цена)
    - date_range: число (например, 7 для последних 7 дней)
    - sort_by: строка для сортировки (например, '-quantity_sold', 'price', '-price' и т.д.)
    - page: номер страницы для пагинации
    """

    # Получаем GET-параметры
    category = request.GET.get('category', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    date_range = request.GET.get('date_range', '').strip()
    sort_by = request.GET.get('sort_by', '-quantity_sold')  # По умолчанию сортируем по кол-ву проданного (убывание)
    page_number = request.GET.get('page', '1')

    # Базовый QuerySet
    qs = Product.objects.all()

    # Фильтр по категории
    if category:
        qs = qs.filter(category=category)

    # Фильтр по цене (min_price и max_price)
    if min_price:
        try:
            qs = qs.filter(price__gte=float(min_price))
        except ValueError:
            pass  # Если не число, игнорируем фильтр

    if max_price:
        try:
            qs = qs.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Фильтр по дате добавления (за последние X дней)
    if date_range:
        try:
            days = int(date_range)
            # Пример: date_range=7 -> за последние 7 дней
            from_date = timezone.now() - datetime.timedelta(days=days)
            qs = qs.filter(created_at__gte=from_date)
        except ValueError:
            pass

    # Применяем сортировку
    # Обратите внимание, что в шаблоне мы передаём sort_by как, например, "-price" или "price"
    # Django корректно распознает префикс "-" для убывающей сортировки.
    if sort_by:
        qs = qs.order_by(sort_by)

    # Пагинация
    # Показываем по 10 товаров на страницу
    paginator = Paginator(qs, 10)

    # Получаем нужную страницу
    page_obj = paginator.get_page(page_number)

    # Формируем список словарей с данными о товаре,
    # которые отправим в формате JSON
    products_data = []
    for product in page_obj:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),  # Сконвертируем Decimal в строку
            'category': product.category,  # Сырой код категории (например 'bouquet')
            'category_display': product.get_category_display(),  # "Человеко-читаемое" название категории
            'quantity_sold': product.quantity_sold,
            'availability_status': product.get_availability_status(),
        })

    # Сформируем ответ
    data = {
        # Список товаров
        'products': products_data,
        # Текущая страница
        'page': page_obj.number,
        # Общее число страниц
        'num_pages': paginator.num_pages,
        # При необходимости можно добавить ссылки на первую, предыдущую и т.д.,
        # если хотите обновлять пагинацию тоже через AJAX.
    }

    return JsonResponse(data, safe=False)
