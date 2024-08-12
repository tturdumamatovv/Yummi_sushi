from urllib.parse import quote

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Restaurant,
    Delivery,
    Order,
    OrderItem,
    DistancePricing,
    TelegramBotToken,
    PercentCashback,
    Report, WhatsAppChat
)
from apps.services.generate_message import generate_order_message


@admin.register(TelegramBotToken)
class TelegramBotTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(WhatsAppChat)
class WhatsAppChatAdmin(admin.ModelAdmin):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'email', 'opening_hours')
    search_fields = ('name', 'address')
    list_filter = ('opening_hours',)


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user_address', 'delivery_time', 'delivery_fee')
    search_fields = ('restaurant__name', 'user_address__city')
    list_filter = ('delivery_time', 'restaurant')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'restaurant', 'delivery', 'order_time', 'total_amount', 'user', 'order_status', 'is_pickup',
        'order_request_button')
    search_fields = ('user',)
    list_filter = ('order_time', 'order_status', 'restaurant', 'is_pickup')
    list_display_links = ('id', 'user')
    list_editable = ('order_status',)
    readonly_fields = ('user', 'delivery', 'order_source', 'id',)
    inlines = [OrderItemInline]

    def total_amount(self, obj):
        return obj.get_total_amount()

    total_amount.short_description = 'Общая сумма'

    def order_request_button(self, obj):
        distance = obj.delivery.distance_km
        delivery_fee = obj.delivery.delivery_fee
        if obj.is_pickup:
            delivery_info = f"Самовывоз\n"
        else:
            delivery_info = f"Адрес доставки: {obj.delivery.user_address}\n Расстояние: {distance} км\n Стоимость доставки: {delivery_fee} сом\n"

        message = (
            f"Новый заказ #{obj.id}\n"
            f"Пользователь: {obj.user}\n"
            f"Номер: {obj.user.phone_number if obj.user and obj.user.phone_number else 'Номер не указан'}\n"
            f"Ресторан: {obj.restaurant_id}\n"
            f'{delivery_info}'
            f"Общая сумма: {obj.total_amount}"
        )
        url_encoded_message = quote(message)
        phone = WhatsAppChat.objects.first().whatsapp_number

        link = f'https://wa.me/{phone}?text={url_encoded_message}'
        return format_html(
            f'<a style="color: white; background-color: orange;" class="button" target="_blank" href="{link}">WhatsApp</a>')

    order_request_button.short_description = 'Действие'


@admin.register(DistancePricing)
class DistancePricingInline(admin.ModelAdmin):
    pass


@admin.register(PercentCashback)
class PercentCashbackAdmin(admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass
