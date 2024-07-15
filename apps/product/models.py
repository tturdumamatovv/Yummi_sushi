from django.db import models
from django.utils.translation import gettext_lazy as _


class Size(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Название'))
    description = models.CharField(max_length=100, blank=True, verbose_name=_('Описание'))

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Название'))
    description = models.CharField(max_length=100, blank=True, verbose_name=_('Описание'))
    size = models.ManyToManyField(Size, related_name='categories', verbose_name=_('Размеры'))

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Категория'))
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'), blank=True, null=True)
    photo = models.ImageField(upload_to='topping_photos/', verbose_name=_('Фото'), blank=True, null=True)
    ingredients = models.ManyToManyField('Ingredient', related_name='products', verbose_name=_('Ингредиенты'))
    toppings = models.ManyToManyField('Topping', related_name='products', verbose_name=_('Добавки'))
    bonuses = models.BooleanField(default=False, verbose_name=_('Можно оптатить бонусами'))

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_sizes',
                                verbose_name=_('Продукт'))
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='product_sizes', verbose_name=_('Размер'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))

    class Meta:
        verbose_name = "Цена продукта по размеру"
        verbose_name_plural = "Цены продуктов по размерам"

    def __str__(self):
        return f"{self.product.name} - {self.size.name} - {self.price}"


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    photo = models.ImageField(upload_to='topping_photos/', verbose_name=_('Фото'), blank=True, null=True)
    possibly_remove = models.BooleanField(default=False, verbose_name=_('Возможность удаления'))

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))
    photo = models.ImageField(upload_to='topping_photos/', verbose_name=_('Фото'), blank=True, null=True)
    bonuses = models.BooleanField(default=False, verbose_name=_('Можно оптатить бонусами'))

    class Meta:
        verbose_name = "Добавка"
        verbose_name_plural = "Добавки"

    def __str__(self):
        return self.name


class Set(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'), blank=True, null=True)
    photo = models.ImageField(upload_to='topping_photos/', verbose_name=_('Фото'), blank=True, null=True)
    products = models.ManyToManyField(ProductSize, related_name='sets', verbose_name=_('Продукты'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))
    bonuses = models.BooleanField(default=False, verbose_name=_('Можно оптатить бонусами'))

    class Meta:
        verbose_name = "Сет"
        verbose_name_plural = "Сеты"

    def __str__(self):
        return self.name