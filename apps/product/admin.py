from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
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


@admin.register(Category)
class CategoryAdmin(ExcludeBaseFieldsMixin, TranslationAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    exclude_base_fields = ('name', 'description')


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
class ProductAdmin(ExcludeBaseFieldsMixin, TranslationAdmin):
    list_display = ('name', 'category', 'description')
    search_fields = ('name',)
    list_filter = ('category',)
    filter_horizontal = ('toppings', 'tags',)  #'ingredients')
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
