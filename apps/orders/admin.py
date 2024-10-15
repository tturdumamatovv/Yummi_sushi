from urllib.parse import quote
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from django.contrib import messages

from .models import (
    Restaurant,
    Delivery,
    Order,
    OrderItem,
    DistancePricing,
    TelegramBotToken,
    PercentCashback,
    Report,
    WhatsAppChat,
    PromoCode,
)
from apps.services.generate_message import generate_order_message


@admin.register(TelegramBotToken)
class TelegramBotTokenAdmin(ModelAdmin):
    pass


@admin.register(WhatsAppChat)
class WhatsAppChatAdmin(ModelAdmin):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(ModelAdmin):
    list_display = ("name", "address", "phone_number", "email", "opening_hours")
    search_fields = ("name", "address")
    list_filter = ("opening_hours",)


@admin.register(Delivery)
class DeliveryAdmin(ModelAdmin):
    list_display = ("restaurant", "user_address", "delivery_time", "delivery_fee")
    search_fields = ("restaurant__name", "user_address__city")
    list_filter = ("delivery_time", "restaurant")
    list_per_page = 10


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        "order_read_status",
        "id",
        "restaurant",
        "delivery",
        "order_time",
        "total_amount",
        "link_to_user",
        "order_status",
        "is_pickup",
        "order_copy_button",
        "order_request_button",
    )
    search_fields = ("user__phone_number",)
    list_filter = ("order_time", "order_status", "restaurant", "is_pickup", "is_read")
    list_display_links = (
        "id",
        "restaurant",
        "delivery",
        "order_time",
        "total_amount",
        "link_to_user",
    )
    list_editable = ("order_status",)
    readonly_fields = (
        "user",
        "delivery",
        "order_source",
        "id",
        "is_read",
    )
    inlines = [OrderItemInline]
    list_per_page = 10

    def total_amount(self, obj):
        return obj.get_total_amount()

    total_amount.short_description = "Общая сумма"

    def link_to_user(self, obj):
        # return 1
        return format_html(
            '<a href="{}">{}</a>',
            obj.user.get_admin_url() if obj.user else "",
            obj.user,
        )

    link_to_user.short_description = "Пользователь"

    def order_request_button(self, obj):
        # Инициализация переменной с пустой строкой
        url_encoded_message = ""

        # Получаем расстояние и стоимость доставки, если они доступны
        distance = obj.delivery.distance_km if obj.delivery else None
        delivery_fee = obj.delivery.delivery_fee if obj.delivery else None

        # Генерируем сообщение, если есть доставка и стоимость
        if distance and delivery_fee:
            message = generate_order_message(obj, distance, delivery_fee)
            url_encoded_message = quote(message)  # Кодируем сообщение для URL

        # Получаем номер WhatsApp, если он существует
        phone = WhatsAppChat.objects.first()
        if not phone:
            return format_html("")

        # Создаём ссылку на WhatsApp
        link = f"https://wa.me/{phone.whatsapp_number}?text={url_encoded_message}"
        return format_html(
            f'<a style="color: white; background-color: orange; padding: 4px 8px; border-radius: 5px; text-decoration: none;" class="button" target="_blank" href="{link}">WhatsApp</a>'
        )

    order_request_button.short_description = "Действие"

    def order_copy_button(self, obj):
        # Инициализация переменной с пустой строкой
        url_encoded_message = ""

        # Получаем расстояние и стоимость доставки, если они доступны
        distance = obj.delivery.distance_km if obj.delivery else None
        delivery_fee = obj.delivery.delivery_fee if obj.delivery else None

        # Генерируем сообщение, если есть доставка и стоимость
        message = generate_order_message(obj, distance, delivery_fee)
        url_encoded_message = quote(message)

        copy_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-copy"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>'
        check_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check"><path d="M20 6 9 17l-5-5"/></svg>'

        script = f"""
        <script>
        function copyToClipboard(text, buttonId) {{
            navigator.clipboard.writeText(decodeURIComponent(text)).then(function() {{
                var button = document.getElementById(buttonId);
                button.innerHTML = '{check_svg}';
                
                // Создаем и показываем всплывающее сообщение
                var popup = document.createElement('div');
                popup.textContent = '{_("Скопировано")}';
                popup.style.position = 'fixed';
                popup.style.left = '50%';
                popup.style.top = '10%';
                popup.style.transform = 'translate(-50%, -50%)';
                popup.style.padding = '10px 20px';
                popup.style.backgroundColor = '#4CAF50';
                popup.style.color = 'white';
                popup.style.borderRadius = '5px';
                popup.style.zIndex = '1000';
                document.body.appendChild(popup);
                
                // Удаляем всплывающее сообщение и возвращаем исходную иконку через 2 секунды
                setTimeout(function() {{
                    document.body.removeChild(popup);
                    button.innerHTML = '{copy_svg}';
                }}, 2000);
            }});
        }}
        </script>
        """

        button_id = f"copy_button_{obj.id}"
        button_html = f"<button id=\"{button_id}\" onclick=\"copyToClipboard('{url_encoded_message}', '{button_id}')\">{copy_svg}</button>"

        return mark_safe(script + button_html)

    order_copy_button.short_description = _("Копия")

    # Логика обозначения прочитано или нет
    def order_read_status(self, obj):
        if obj.is_read:
            return format_html(
                '<div style="display: flex; align-items: center; justify-content: center; width: 24px; height: 24px;"><div class="no-animation" /></div>'
            )
        else:
            return format_html(
                '<div style="display: flex; align-items: center; justify-content: center; width: 24px; height: 24px; position: relative;"><div class="no-animation-red" /> <div class="animate-ping" /></div>'
            )

    order_read_status.short_description = "👁️"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.is_read:
            obj.is_read = True
            obj.save()
            messages.info(request, "Заказ отмечен как прочитанный.")
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )


@admin.register(DistancePricing)
class DistancePricingInline(ModelAdmin):
    pass


@admin.register(PercentCashback)
class PercentCashbackAdmin(ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(ModelAdmin):
    pass


@admin.register(PromoCode)
class PromoCodeAdmin(ModelAdmin):
    list_display = ["code", "discount", "valid_from", "valid_to", "active", "type"]
    list_filter = ["active", "valid_from", "valid_to"]
    search_fields = ["code"]
