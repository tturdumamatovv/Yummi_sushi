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
    Report
)


@admin.register(TelegramBotToken)
class TelegramBotTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'email', 'opening_hours')
    search_fields = ('name', 'address')
    list_filter = ('opening_hours',)


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('restaurant',  'user_address', 'delivery_time', 'delivery_fee')
    search_fields = ('restaurant__name', 'user_address__city')
    list_filter = ('delivery_time', 'restaurant')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'restaurant', 'delivery', 'order_time', 'total_amount', 'user', 'order_status', 'is_pickup', 'order_request_button')
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
        # ссылка на ваш view, который обрабатывает запрос, с передачей ID заказа
        link = '#'
        return format_html(f'<a style="color: white; background-color: orange;" class="button" target="_blank" href="{link}">Запрос</a>')

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
