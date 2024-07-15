# serializers.py
from rest_framework import serializers
from apps.orders.models import Order, OrderItem, Delivery
from apps.product.models import ProductSize, Set


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['id', 'product', 'size', 'price']


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ['id', 'name', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    product_size = ProductSizeSerializer()
    set = SetSerializer()

    class Meta:
        model = OrderItem
        fields = ['product_size', 'set', 'quantity', 'total_amount']


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['restaurant', 'user_address', 'delivery_time', 'delivery_fee']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    delivery = DeliverySerializer()

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'delivery', 'order_time', 'total_amount', 'is_pickup', 'order_status',
                  'order_items']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        delivery_data = validated_data.pop('delivery')
        user = validated_data.pop('user')
        delivery = Delivery.objects.create(**delivery_data)
        order = Order.objects.create(delivery=delivery, user=user, **validated_data)
        for order_item_data in order_items_data:
            product_size = order_item_data.pop('product_size', None)
            set = order_item_data.pop('set', None)
            if product_size:
                product_size_instance = ProductSize.objects.get(id=product_size['id'])
                OrderItem.objects.create(order=order, product_size=product_size_instance, **order_item_data)
            if set:
                set_instance = Set.objects.get(id=set['id'])
                OrderItem.objects.create(order=order, set=set_instance, **order_item_data)
        return order
