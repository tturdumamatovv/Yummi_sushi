# serializers.py
from rest_framework import serializers
from apps.product.models import Product, ProductSize, Ingredient, Topping, Set


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'photo', 'possibly_remove']


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ['name', 'price', 'photo', 'bonuses']


class ProductSizeSerializer(serializers.ModelSerializer):
    size = serializers.StringRelatedField()

    class Meta:
        model = ProductSize
        fields = ['id', 'size', 'price']


class ProductSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    toppings = ToppingSerializer(many=True)
    product_sizes = ProductSizeSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'photo', 'ingredients', 'toppings', 'product_sizes', 'bonuses']


class SizeProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    size = serializers.StringRelatedField()

    class Meta:
        model = ProductSize
        fields = ['product', 'size', 'price']


class SetSerializer(serializers.ModelSerializer):
    products = SizeProductSerializer(many=True)

    class Meta:
        model = Set
        fields = ['id', 'name', 'description', 'photo', 'products', 'price', 'bonuses']
