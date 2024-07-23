# translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, Ingredient, Topping, Size  # Set,


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Ingredient)
class IngredientTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Topping)
class ToppingTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Size)
class SizeTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


# @register(Set)
# class SetTranslationOptions(TranslationOptions):
#     fields = ('name', 'description')

