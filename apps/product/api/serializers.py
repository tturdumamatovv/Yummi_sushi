# serializers.py
from rest_framework import serializers
from apps.product.models import Product, ProductSize, Topping, Category, Tag  # Set, Ingredient


# class IngredientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ingredient
#         fields = ['name', 'photo', 'possibly_remove']


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ['id', 'name', 'price', 'photo']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['price'] = float(representation['price'])
        return representation


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'text_color', 'background_color']


class ProductSizeSerializer(serializers.ModelSerializer):
    size = serializers.StringRelatedField()

    class Meta:
        model = ProductSize
        fields = ['id', 'size', 'price', 'discounted_price']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['price'] = float(representation['price'])
        representation['discounted_price'] = float(representation['discounted_price']) if representation[
                                                                                              'discounted_price'] is not None else None
        return representation


class ProductSerializer(serializers.ModelSerializer):
    # ingredients = IngredientSerializer(many=True)
    toppings = ToppingSerializer(many=True)
    tags = TagSerializer(many=True)
    product_sizes = ProductSizeSerializer(many=True)
    min_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'photo', 'tags', 'toppings', 'min_price', 'bonuses',
                  'product_sizes']

    def get_min_price(self, obj):
        return obj.get_min_price()


class SizeProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    size = serializers.StringRelatedField()

    class Meta:
        model = ProductSize
        fields = ['product', 'size', 'price', 'discounted_price']


class SetProductSerializer(serializers.ModelSerializer):
    # ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'photo', ]  # 'ingredients', ]


class ComboProductSerializer(serializers.ModelSerializer):
    product = SetProductSerializer()
    size = serializers.StringRelatedField()

    class Meta:
        model = ProductSize
        fields = ['product', 'size', 'price', 'discounted_price']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['price'] = float(representation['price'])
        representation['discounted_price'] = float(representation['discounted_price']) if representation[
                                                                                              'discounted_price'] is not None else None
        return representation


# class SetSerializer(serializers.ModelSerializer):
#     products = ComboProductSerializer(many=True)
#
#     class Meta:
#         model = Set
#         fields = ['id', 'name', 'description', 'photo', 'products', 'price', 'discounted_price', 'bonuses']

# def to_representation(self, instance):
#     representation = super().to_representation(instance)
#     representation['price'] = float(representation['price'])
#     representation['discounted_price'] = float(representation['discounted_price']) if representation[
#                                                                                           'discounted_price'] is not None else None
#     return representation


class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    # sets = SetSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'image', 'products', ]  # 'sets']


class CategoryOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'image', ]


class ProductSizeWithBonusSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_description = serializers.CharField(source='product.description')
    product_photo = serializers.ImageField(source='product.photo')

    class Meta:
        model = ProductSize
        fields = ['product_name', 'product_description', 'product_photo', 'size', 'bonus_price']
