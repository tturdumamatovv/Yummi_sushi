from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from mptt.admin import DraggableMPTTAdmin

from .models import Size, Category, Product, ProductSize, Topping, Tag  # Set, Ingredient
from .forms import ProductSizeForm


class ExcludeBaseFieldsMixin:
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        base_fields = getattr(self, 'exclude_base_fields', [])
        for field_name in base_fields:
            if field_name in form.base_fields:
                del form.base_fields[field_name]
        return form


@admin.register(Size)
class SizeAdmin(ExcludeBaseFieldsMixin, TranslationAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    exclude_base_fields = ('name', 'description')

Category.objects.rebuild()


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin, ExcludeBaseFieldsMixin, TranslationAdmin):
    list_display = ('tree_actions', 'indented_name', 'description')
    list_display_links = ('indented_name',)
    search_fields = ('name',)
    exclude_base_fields = ('name', 'description')
    mptt_level_indent = 30  # Увеличенный отступ для более заметной вложенности

    def indented_name(self, instance):
        """
        Возвращает отступленное название категории, основываясь на уровне вложенности.
        Отступ рассчитывается как умножение mptt_level_indent на уровень вложенности.
        """
        level = instance._mpttfield('level') * self.mptt_level_indent
        return format_html('<div style="padding-left:{}px;">{}</div>', level, instance.name)
    indented_name.short_description = "Название"  # Или любой другой текст в соответствии с вашим языком


@admin.register(Tag)
class TagAdmin(ExcludeBaseFieldsMixin, TranslationAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    exclude_base_fields = ('name',)


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    form = ProductSizeForm
    extra = 0


@admin.register(Product)
class ProductAdmin(SortableAdminMixin, ExcludeBaseFieldsMixin, TranslationAdmin):
    list_display = ('name', 'category', 'description')
    search_fields = ('name',)
    list_filter = ('category',)
    filter_horizontal = ('toppings', 'tags',)  # 'ingredients')
    inlines = [ProductSizeInline]
    exclude_base_fields = ('name', 'description')


@admin.register(Topping)
class ToppingAdmin(ExcludeBaseFieldsMixin, TranslationAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    exclude_base_fields = ('name',)


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
