import random
import string
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from geopy.distance import geodesic

from apps.authentication.models import UserAddress
from apps.pages.models import SingletonModel
from apps.product.models import ProductSize, Topping  # Set,Ingredient


class WhatsAppChat(SingletonModel):
    whatsapp_number = models.CharField(max_length=200, unique=True, verbose_name=_("Телеграм Бот Токен"))
    def __str__(self):
        return f"{self.whatsapp_number}"

    class Meta:
        verbose_name = _("Номер WhatsApp")
        verbose_name_plural = _("Номер WhatsApp")


class TelegramBotToken(models.Model):
    bot_token = models.CharField(max_length=200, unique=True, verbose_name=_("Телеграм Бот Токен"))
    report_channels = models.TextField(max_length=200, blank=True, null=True, verbose_name=_("Айди каналов"))
    app_download_link = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Ссылка на приложение"))
    google_map_api_key = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Ключ для карты"))

    def clean(self):
        if TelegramBotToken.objects.exists() and not self.pk:
            raise ValidationError(_('Может существовать только один экземпляр модели TelegramBotToken.'))

    def save(self, *args, **kwargs):
        self.pk = 1  # Гарантирует, что всегда существует только один экземпляр
        super().save(*args, **kwargs)

    def __str__(self):
        return "Токен бота Telegram"

    class Meta:
        verbose_name = _("Токен бота Telegram")
        verbose_name_plural = _("Токены бота Telegram")


class Restaurant(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    address = models.CharField(max_length=255, verbose_name=_('Адрес'))
    phone_number = models.CharField(max_length=15, verbose_name=_('Телефонный номер'), blank=True, null=True)
    email = models.EmailField(verbose_name=_('Электронная почта'), blank=True, null=True)
    opening_hours = models.TimeField(verbose_name=_('Время открытия'), blank=True, null=True)
    closing_hours = models.TimeField(verbose_name=_('Время закрытия'), blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('Широта'), blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('Долгота'), blank=True, null=True)
    telegram_chat_ids = models.TextField(verbose_name=_('Telegram Chat IDs'), validators=[MinLengthValidator(1)],
                                         help_text=_('Введите чат-айди через запятую'), blank=True, null=True)
    self_pickup_available = models.BooleanField(default=True, verbose_name=_('Самовывоз доступен'))

    class Meta:
        verbose_name = _("Ресторан")
        verbose_name_plural = _("Рестораны")

    def __str__(self):
        return self.name

    def get_telegram_chat_ids(self):
        if self.telegram_chat_ids:
            return [chat_id.strip() for chat_id in self.telegram_chat_ids.split(',') if chat_id.strip()]
        return []

    def distance_to(self, user_lat, user_lon):
        restaurant_location = (self.latitude, self.longitude)
        user_location = (user_lat, user_lon)
        return geodesic(restaurant_location, user_location).kilometers


class Delivery(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name=_('Ресторан'))
    user_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, verbose_name=_('Адрес пользователя'),
                                     blank=True, null=True)
    delivery_time = models.DateTimeField(verbose_name=_('Время доставки'), blank=True, null=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Стоимость доставки')
                                       , blank=True, null=True)
    distance_km = models.CharField(max_length=10, verbose_name=_('Расстояние (км)'), blank=True, null=True)

    class Meta:
        verbose_name = _("Доставка")
        verbose_name_plural = _("Доставки")

    def __str__(self):
        return f" {'Доставка ' + self.user_address.city if self.user_address else 'Самовывоз'} от {self.restaurant.name}"


class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name=_('Ресторан'))
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, verbose_name=_('Доставка'), blank=True, null=True)
    order_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Время заказа'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Общая сумма'), blank=True,
                                       null=True)
    total_bonus_amount = models.IntegerField(verbose_name=_('Общая сумма бонусов'), blank=True, null=True)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='orders', verbose_name=_('Пользователь')
                             , blank=True, null=True)
    is_pickup = models.BooleanField(default=False, verbose_name=_('Самовывоз'))
    payment_method = models.CharField(
        max_length=255,
        choices=[('card', 'Карта'),
                 ('cash', 'Наличные'),
                 ('online', 'Онлайн'),
                 ],
        default='card',
        verbose_name=_('Способ оплаты')
    )
    change = models.IntegerField(verbose_name=_('Сдача'), blank=True, null=True)

    order_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', _('В ожидании')),
            ('in_progress', _('В процессе')),
            ('delivery', _('Доставка')),
            ('completed', _('Завершено')),
            ('cancelled', _('Отменено'))
        ],
        default='pending',
        verbose_name=_('Статус заказа')
    )
    order_source = models.CharField(
        max_length=10,
        choices=[
            ('mobile', 'Мобильное приложение'),
            ('web', 'Веб-сайт'),
            ('unknown', 'Неизвестно')
        ],
        default='unknown',
        verbose_name=_('Источник заказа')
    )
    comment = models.TextField(verbose_name=_('Комментарий'), blank=True, null=True)
    promo_code = models.ForeignKey('PromoCode', on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    def __str__(self):
        return f"Заказ #{self.id}"

    def apply_promo_code(self):
        if self.promo_code and self.promo_code.is_valid():
            if self.promo_code.type == 'p':
                discount_rate = Decimal(self.promo_code.discount) / Decimal(100)
                discount_amount = discount_rate * self.total_amount
            elif self.promo_code.type == 'f':
                discount_amount = Decimal(self.promo_code.discount)
            discount_amount = min(discount_amount, self.total_amount)
            return self.total_amount - discount_amount
        return self.total_amount

    def get_total_amount(self):
        total_amount = self.delivery.delivery_fee
        for order_item in self.order_items.all():
            total_amount += order_item.total_amount
        return total_amount

    def get_total_amount_2(self):
        total_amount = self.delivery.delivery_fee
        for order_item in self.order_items.all():
            total_amount += order_item.calculate_total_amount()
        return total_amount

    def get_total_bonus_amount(self):
        total_bonus_amount = self.total_bonus_amount
        if total_bonus_amount is None:
            total_bonus_amount = 0
        for order_item in self.order_items.filter(is_bonus=True):
            total_bonus_amount += order_item.total_amount

        return total_bonus_amount

    def get_order_status_display(self):
        return dict(Order.ORDER_STATUS_CHOICES)[self.order_status]

    def save(self, *args, **kwargs):
        self.total_amount = self.apply_promo_code()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name=_('Заказ'))
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, verbose_name=_('Размер продукта'),
                                     blank=True, null=True)
    topping = models.ManyToManyField(Topping, blank=True, verbose_name=_('Добавки'))
    quantity = models.PositiveIntegerField(verbose_name=_('Количество'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Общая сумма'))
    is_bonus = models.BooleanField(default=False, verbose_name=_('Бонусный продукт'))

    # excluded_ingredient = models.ManyToManyField(Ingredient, blank=True,
    #                                              verbose_name=_('Исключенные ингредиенты'))
    # set = models.ForeignKey(Set, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Сет'))

    class Meta:
        verbose_name = _("Элемент заказа")
        verbose_name_plural = _("Элементы заказа")

    def __str__(self):
        return f"{self.product_size.product.name if self.product_size else self.set.name} ({self.product_size.size.name if self.product_size else 'Сет'}) - {self.quantity} шт."



    def calculate_total_amount(self):
        if not self.is_bonus:
            total = self.quantity * (self.product_size.get_price() if self.product_size else self.set.get_price())
            for topping in self.topping.all():
                total += topping.price * self.quantity
            return total
        else:
            total = self.quantity * (self.product_size.bonus_price if self.product_size else self.set.bonus_price)
            for topping in self.topping.all():
                total += topping.price * self.quantity
            return total

    def save(self, *args, **kwargs):
        if not self.id:
            self.total_amount = 0
            super().save(*args, **kwargs)
        self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)
        self.order.total_amount = self.order.get_total_amount()
        if self.is_bonus:
            self.order.total_bonus_amount = self.order.get_total_bonus_amount()
        self.order.save()


class DistancePricing(models.Model):
    distance = models.IntegerField(verbose_name=_("Расстояние (км)"))
    price = models.IntegerField(verbose_name=_("Цена"))

    def __str__(self):
        return f"{self.distance} км - {self.price} сом"

    class Meta:
        verbose_name = _("Тариф на расстояние")
        verbose_name_plural = _("Тарифы на расстояния")


class PercentCashback(SingletonModel):
    mobile_percent = models.IntegerField(verbose_name=_("Процент за мобильное приложение"))
    web_percent = models.IntegerField(verbose_name=_("Процент за веб-сайт"))

    def __str__(self):
        return f"Процент кэшбека № {self.id}"

    class Meta:
        verbose_name = _("Процент кэшбэка")
        verbose_name_plural = _("Проценты кэшбэка")


class Report(models.Model):
    image = models.ImageField(upload_to='reports/', blank=True, null=True, verbose_name=_("Картинка"))
    description = models.TextField(verbose_name=_("Описание"))
    contact_number = models.CharField(max_length=15, verbose_name=_("Контактный номер"))

    def __str__(self):
        return f"Отчет № {self.id}"

    class Meta:
        verbose_name = _("Отчет")
        verbose_name_plural = _("Отчеты")


class PromoCode(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='Промокод')
    valid_from = models.DateTimeField(verbose_name='Начало действия')
    valid_to = models.DateTimeField(verbose_name='Конец действия')
    discount = models.IntegerField(help_text='Процент скидки', verbose_name='Скидка')
    active = models.BooleanField(default=False, verbose_name='Активен')
    type = models.CharField(max_length=3, choices=[('%', 'Процент'), ('сом', 'Фиксированная сумма')], verbose_name='Тип')

    def __str__(self):
        return self.code

    @staticmethod
    def generate_code(length=6):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    def is_valid(self):
        from django.utils import timezone
        return self.active and self.valid_from <= timezone.now() <= self.valid_to