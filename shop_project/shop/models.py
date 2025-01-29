# shop_project\shop\models.py
from django.db import models

class Product(models.Model):
    # Пример категорий — можно хранить в виде текстовых значений
    # или вынести в отдельную модель Category (при необходимости).
    CATEGORY_CHOICES = [
        ('bouquet', 'Букеты'),
        ('single', 'Одиночные цветы'),
        ('composition', 'Композиции'),
        # Добавляйте свои варианты...
    ]

    name = models.CharField(
        max_length=255,
        verbose_name="Название"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name="Категория"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )
    quantity_sold = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество реализованных заказов"
    )
    available_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество доступное для заказа"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name="Изображение",
        blank=True
    )

    def __str__(self):
        return self.name

    @property
    def is_available(self):
        """
        Возвращает True, если товар доступен (осталось > 0),
        иначе False.
        """
        return self.available_quantity > 0

    def get_availability_status(self):
        """
        Возвращает строку "Доступен" или "Не доступен" в зависимости от количества.
        Можно использовать в шаблонах.
        """
        return "Доступен" if self.is_available else "Не доступен"
