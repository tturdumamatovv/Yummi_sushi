from django.contrib import admin
from .models import Size, Category, Product, ProductSize, Ingredient, Topping
from .forms import ProductSizeForm

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    filter_horizontal = ('size',)

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    form = ProductSizeForm
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    search_fields = ('name',)
    list_filter = ('category',)
    filter_horizontal = ('toppings', 'ingredients')
    inlines = [ProductSizeInline]

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
