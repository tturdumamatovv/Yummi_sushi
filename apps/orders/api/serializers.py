# serializers.py
from django.db import transaction
from rest_framework import serializers
from apps.orders.models import Order, OrderItem, Delivery, Topping, Ingredient, Restaurant
from apps.product.models import ProductSize, Set
from apps.authentication.models import UserAddress


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id']


class ProductOrderItemSerializer(serializers.ModelSerializer):
    product_size_id = serializers.IntegerField(write_only=True)
    topping_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    excluded_ingredient_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = OrderItem
        fields = ['product_size_id', 'quantity', 'topping_ids', 'excluded_ingredient_ids']

    def validate(self, data):
        if data.get('product_size_id') == 0:
            raise serializers.ValidationError("Invalid product_size_id.")
        return data


class SetOrderItemSerializer(serializers.ModelSerializer):
    set_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['set_id', 'quantity']

    def validate(self, data):
        if data.get('set_id') == 0:
            raise serializers.ValidationError("Invalid set_id.")
        return data


class DeliverySerializer(serializers.ModelSerializer):
    user_address_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Delivery
        fields = ['user_address_id', 'delivery_time']


class OrderSerializer(serializers.ModelSerializer):
    products = ProductOrderItemSerializer(many=True, required=False)
    sets = SetOrderItemSerializer(many=True, required=False)
    restaurant_id = serializers.IntegerField(required=False, allow_null=True)
    delivery = DeliverySerializer()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'delivery', 'order_time', 'total_amount', 'is_pickup',
            'order_status', 'products', 'sets', 'payment_method', 'change', 'restaurant_id',
        ]
        read_only_fields = ['total_amount', 'order_time', 'order_status']

    def create(self, validated_data):
        print(validated_data)
        products_data = validated_data.pop('products', [])
        sets_data = validated_data.pop('sets', [])
        delivery_data = validated_data.pop('delivery')
        user = validated_data.pop('user')

        user_address = UserAddress.objects.get(id=delivery_data['user_address_id'])
        nearest_restaurant = self.context['nearest_restaurant']
        delivery_fee = self.context['delivery_fee']

        with transaction.atomic():
            delivery = Delivery.objects.create(
                restaurant=nearest_restaurant,
                user_address=user_address,
                delivery_time=delivery_data['delivery_time'],
                delivery_fee=delivery_fee
            )

            order = Order.objects.create(
                delivery=delivery,
                user=user,
                restaurant=nearest_restaurant,
                **validated_data
            )

            for product_data in products_data:
                topping_ids = product_data.pop('topping_ids', [])
                excluded_ingredient_ids = product_data.pop('excluded_ingredient_ids', [])

                order_item = OrderItem(order=order, product_size_id=product_data['product_size_id'],
                                       quantity=product_data['quantity'])
                order_item.save()

                if topping_ids:
                    toppings = Topping.objects.filter(id__in=topping_ids)
                    order_item.topping.set(toppings)
                order_item.save()
                if excluded_ingredient_ids:
                    excluded_ingredients = Ingredient.objects.filter(id__in=excluded_ingredient_ids)
                    order_item.excluded_ingredient.set(excluded_ingredients)

            for set_data in sets_data:
                set_order_item = OrderItem(order=order, set_id=set_data['set_id'], quantity=set_data['quantity'])
                set_order_item.save()

        return order


class ProductOrderItemPreviewSerializer(serializers.Serializer):
    product_size_id = serializers.IntegerField(write_only=True)
    topping_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    excluded_ingredient_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    quantity = serializers.IntegerField()


class SetOrderItemPreviewSerializer(serializers.Serializer):
    set_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField()


class OrderPreviewSerializer(serializers.Serializer):
    user_address_id = serializers.IntegerField()
    is_pickup = serializers.BooleanField(default=False)
    payment_method = serializers.ChoiceField(choices=[('card', 'Карта'),
                                                      ('cash', 'Наличные'),
                                                      ('online', 'Онлайн'), ])
    products = ProductOrderItemPreviewSerializer(many=True, required=False)
    sets = SetOrderItemPreviewSerializer(many=True, required=False)
