from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Электронная почта")
    address = models.CharField(max_length=250, verbose_name="Адрес")
    postal_code = models.CharField(max_length=20, verbose_name="Почтовый индекс")
    city = models.CharField(max_length=100, verbose_name="Город")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    # Лучше поле переименовать в 'succeeded'
    paid = models.BooleanField(default=False, verbose_name="Оплачен (Одобрен администратором и успешен)")
    waiting_for_capture = models.BooleanField(default=False, verbose_name="Ожидает подтверждения оплаты администратором")
    canceled = models.BooleanField(default=False, verbose_name="Отменен")

    total_price = models.DecimalField(null=True, max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")

    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)], verbose_name="Скидка")

    yookassa_id = models.CharField(max_length=150, blank=True, verbose_name="ID платежа")

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))



class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity