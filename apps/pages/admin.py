from django.contrib import admin

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
    list_display = ["title", "link", "is_active", "created_at"]
    list_filter = ["title", "is_active", "created_at"]
    search_fields = ["title", "link", "created_at"]
    date_hierarchy = "created_at"
    fields = (
        "title",
        "link",
        "image_desktop",
        "get_image_desktop",
        "image_mobile",
        "get_image_mobile",
        "is_active",
        "created_at",
    )
    readonly_fields = ("get_image_desktop", "get_image_mobile", "created_at")


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('title',)
    fieldsets = (
        (None, {
            'fields': ('title_ru', 'title_ky', 'description_ru', 'description_ky', 'image')
        }),
        ('Расширенные параметры', {
            'fields': ('slug', 'meta_title', 'meta_description', 'meta_image'),
        }),
    )


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
