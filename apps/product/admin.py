from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from unfold.admin import TabularInline, ModelAdmin

from .models import (
    Size,
    Category,
    Product,
    ProductSize,
    Topping,
    Tag,
)  # Set, Ingredient
from .forms import ProductSizeForm


class ExcludeBaseFieldsMixin(ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        base_fields = getattr(self, "exclude_base_fields", [])
        for field_name in base_fields:
            if field_name in form.base_fields:
                del form.base_fields[field_name]
        return form


@admin.register(Size)
class SizeAdmin(ExcludeBaseFieldsMixin, TranslationAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    exclude_base_fields = ("name", "description")


@admin.register(Tag)
class TagAdmin(ExcludeBaseFieldsMixin, TranslationAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    exclude_base_fields = ("name",)


class ProductSizeInline(TabularInline):
    model = ProductSize
    form = ProductSizeForm
    extra = 0


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, ExcludeBaseFieldsMixin, TranslationAdmin):
    list_display = ("name", "description", "order")
    search_fields = ("name",)
    exclude_base_fields = ("name", "description")


@admin.register(Product)
class ProductAdmin(SortableAdminMixin, ExcludeBaseFieldsMixin, TranslationAdmin):
    list_display = ("order", "name", "category", "description")
    search_fields = ("name",)
    list_filter = ("category",)
    filter_horizontal = (
        "toppings",
        "tags",
    )  # 'ingredients')
    inlines = [ProductSizeInline]
    exclude_base_fields = ("name", "description")
    list_per_page = 25


@admin.register(Topping)
class ToppingAdmin(ExcludeBaseFieldsMixin, TranslationAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)
    exclude_base_fields = ("name",)


# @admin.register(Set)
# class SetAdmin(ExcludeBaseFieldsMixin, TranslationAdmin):
#     list_display = ('name', 'description')
#     search_fields = ('name', 'description')
#     filter_horizontal = ('products',)
#     list_filter = ('products',)
#     exclude_base_fields = ('name', 'description')


# @admin.register(Ingredient)
# class IngredientAdmin(ExcludeBaseFieldsMixin, TranslationAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)
#     exclude_base_fields = ('name',)
