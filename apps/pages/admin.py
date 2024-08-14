from django.contrib import admin
from django.utils.html import format_html

from apps.pages.models import (
    Banner,
    Phone,
    StaticPage,
    Email,
    SocialLink,
    PaymentMethod,
    Address,
    Contacts,
    MethodsOfPayment,
    DeliveryConditions,
    OrderTypes,
    MainPage
)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", "type", 'object_link', "is_active", "created_at"]
    list_filter = ["title", "is_active", "created_at"]
    search_fields = ["title", "link", "created_at"]
    date_hierarchy = "created_at"
    fields = (
        "type",
        "product",
        "category",
        "link",
        "title",
        "image_desktop",
        "get_image_desktop",
        "image_mobile",
        "get_image_mobile",
        "is_active",
        "created_at",
    )
    readonly_fields = ("get_image_desktop", "get_image_mobile", "created_at")

    def object_link(self, obj):
        if obj.type == 'category' and obj.category:
            # Ссылка на категорию, предполагается что у категории есть метод get_absolute_url()
            return format_html('<a href="{}">{}</a>', obj.category.get_absolute_url(), obj.category)
        elif obj.type == 'product' and obj.product:
            # Ссылка на продукт, предполагается что у продукта есть метод get_absolute_url()
            return format_html('<a href="{}">{}</a>', obj.product.get_absolute_url(), obj.product)
        elif obj.type == 'link' and obj.link:
            # Прямая внешняя ссылка
            return format_html('<a href="{}">{}</a>', obj.link, obj.link)
        return None  # Возвращаем None, если условия не выполняются
    object_link.short_description = "Ссылка объекта"



@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    exclude = [
        'title',
        'description',
    ]


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0


class EmailInline(admin.TabularInline):
    model = Email
    extra = 0


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0


class PaymentMethodLinkInline(admin.TabularInline):
    model = PaymentMethod
    extra = 0


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    pass
    inlines = [PhoneInline, EmailInline, SocialLinkInline, PaymentMethodLinkInline, AddressInline]


class OrderTypesInline(admin.TabularInline):
    model = OrderTypes
    extra = 0


class DeliveryConditionsInline(admin.TabularInline):
    model = DeliveryConditions
    extra = 0


class MethodsOfPaymentInline(admin.TabularInline):
    model = MethodsOfPayment
    extra = 0


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ('phone', 'icon', 'meta_title', 'meta_description', 'meta_image')
    inlines = [OrderTypesInline, DeliveryConditionsInline, MethodsOfPaymentInline]
