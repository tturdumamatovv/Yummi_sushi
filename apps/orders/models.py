import math
from django.db import models
from django.utils.translation import gettext_lazy as _
from geopy.distance import geodesic

from apps.authentication.models import UserAddress
from apps.product.models import ProductSize, Set, Ingredient, Topping


class Restaurant(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    address = models.CharField(max_length=255, verbose_name=_('Адрес'))
    phone_number = models.CharField(max_length=15, verbose_name=_('Телефонный номер'), blank=True, null=True)
    email = models.EmailField(verbose_name=_('Электронная почта'), blank=True, null=True)
    opening_hours = models.CharField(max_length=100, verbose_name=_('Часы работы'), blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('Широта'), blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('Долгота'), blank=True, null=True)

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"

    def __str__(self):
        return self.name

    def distance_to(self, user_lat, user_lon):
        restaurant_location = (self.latitude, self.longitude)
        user_location = (user_lat, user_lon)
        return geodesic(restaurant_location, user_location).kilometers


class Delivery(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name=_('Ресторан'))
    user_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, verbose_name=_('Адрес пользователя'))
    delivery_time = models.DateTimeField(verbose_name=_('Время доставки'))
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Стоимость доставки'))

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"

    def __str__(self):
        return f"Доставка в {self.user_address.city}, {self.user_address.street} от {self.restaurant.name}"


class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name=_('Ресторан'))
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, verbose_name=_('Доставка'))
    order_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Время заказа'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Общая сумма'), blank=True,
                                       null=True)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    is_pickup = models.BooleanField(default=False, verbose_name=_('Самовывоз'))

    order_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', _('В ожидании')),
            ('in_progress', _('В процессе')),
            ('completed', _('Завершено')),
            ('cancelled', _('Отменено'))
        ],
        default='pending',
        verbose_name=_('Статус заказа')
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.full_name}"

    def get_total_amount(self):
        total_amount = self.delivery.delivery_fee
        for order_item in self.order_items.all():
            total_amount += order_item.total_amount
        return total_amount

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name=_('Заказ'))
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, verbose_name=_('Размер продукта'), blank=True, null=True)
    topping = models.ManyToManyField(Topping, blank=True, null=True, verbose_name=_('Добавки'))
    excluded_ingredient = models.ManyToManyField(Ingredient, blank=True, null=True, verbose_name=_('Исключенные ингредиенты'))
    set = models.ForeignKey(Set, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Сет'))
    quantity = models.PositiveIntegerField(verbose_name=_('Количество'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Общая сумма'))

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

    def __str__(self):
        return f"{self.product_size.product.name} ({self.product_size.size.name}) - {self.quantity} шт."

    def calculate_total_amount(self):
        total = self.quantity * (self.product_size.price if self.product_size else self.set.price)
        for topping in self.topping.all():
            total += topping.price * self.quantity
        self.total_amount = total

    def save(self, *args, **kwargs):
        if self.product_size:
            self.total_amount = self.quantity * self.product_size.price
        elif self.set:
            self.total_amount = self.quantity * self.set.price
        super().save(*args, **kwargs)
        self.order.total_amount = self.order.get_total_amount()
        self.order.save()


class DistancePricing(models.Model):
    distance = models.IntegerField(verbose_name="Расстояние (км)")
    price = models.IntegerField(verbose_name="Цена")

    def __str__(self):
        return f"{self.distance} км - {self.price} сом"