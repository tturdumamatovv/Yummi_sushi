import pytz

from django.db import transaction
from django.conf import settings

from rest_framework import serializers

from apps.authentication.models import UserAddress
from apps.orders.models import (
    Order,
    OrderItem,
    Delivery,
    Topping,
    Restaurant,
    Report,
    TelegramBotToken, PromoCode

)  # Ingredient)
from apps.product.models import ProductSize, Product


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ['id', 'name', 'price']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number', 'email', 'opening_hours', 'closing_hours',
                  'latitude', 'longitude', 'self_pickup_available']


class ProductOrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    product_size_id = serializers.IntegerField(write_only=True)
    topping = ToppingSerializer(many=True, read_only=False)  # Список топингов теперь полностью сериализуется
    quantity = serializers.IntegerField(default=0)
    is_bonus = serializers.BooleanField(default=False)

    # excluded_ingredient_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = OrderItem
        fields = ['product_size_id', 'quantity', 'topping', 'is_bonus', 'product']  # , 'excluded_ingredient_ids'

    def validate(self, data):
        if data.get('product_size_id') == 0:
            raise serializers.ValidationError("Invalid product_size_id.")
        return data

    def get_product(self, obj):
        request = self.context.get('request')
        photo_url = obj.product_size.product.photo.url if obj.product_size.product.photo else None
        if photo_url and request:
            photo_url = request.build_absolute_uri(photo_url)
        toppings_list = [topping.id for topping in obj.topping.all()]

        size = {
            'size_id': obj.product_size.id,
            'toppings': toppings_list
        }

        return {
            'id': obj.product_size.product.id,
            'name': obj.product_size.product.name,
            'price': obj.product_size.get_price(),
            'image': photo_url,
            'size': size
        }


# class SetOrderItemSerializer(serializers.ModelSerializer):
#     set_id = serializers.IntegerField(write_only=True)
#
#     class Meta:
#         model = OrderItem
#         fields = ['set_id', 'quantity', 'is_bonus']
#
#     def validate(self, data):
#         if data.get('set_id') == 0:
#             raise serializers.ValidationError("Invalid set_id.")
#         return data
#

class DeliverySerializer(serializers.ModelSerializer):
    user_address_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Delivery
        fields = ['user_address_id']


class OrderListSerializer(serializers.ModelSerializer):
    order_items = ProductOrderItemSerializer(many=True, required=False)
    restaurant = RestaurantSerializer()
    total_amount = serializers.SerializerMethodField()
    order_time = serializers.SerializerMethodField()
    user_address = serializers.SerializerMethodField()
    app_download_url = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'total_amount', 'order_time', 'restaurant', 'order_items', 'total_bonus_amount',
                  'is_pickup', 'user_address', 'app_download_url', 'order_status']

    def get_total_amount(self, obj):
        return obj.get_total_amount_2()

    def get_order_time(self, obj):
        local_tz = pytz.timezone(settings.TIME_ZONE)
        order_time = obj.order_time.astimezone(local_tz)
        return order_time.strftime('%Y-%m-%d %H:%M')

    def get_user_address(self, obj):
        return obj.delivery.user_address.city if obj.delivery.user_address else "Самовывоз"

    def get_app_download_url(self, obj):
        link = TelegramBotToken.objects.first().app_download_link
        if not link:
            return None
        return link


class OrderSerializer(serializers.ModelSerializer):
    products = ProductOrderItemSerializer(many=True, required=False)
    # sets = SetOrderItemSerializer(many=True, required=False)
    restaurant_id = serializers.IntegerField(required=False, allow_null=True)
    delivery = DeliverySerializer(required=False)
    order_source = serializers.ChoiceField(choices=[('web', 'web'), ('mobile', 'mobile')], default='web')
    change = serializers.IntegerField(default=0)
    is_pickup = serializers.BooleanField(default=False)
    promo_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Order
        fields = [
            'id', 'delivery', 'order_time', 'total_amount', 'is_pickup',
            'order_status', 'products', 'payment_method', 'change', 'restaurant_id', 'order_source', 'comment',
            'promo_code'
            # 'sets',
        ]
        read_only_fields = ['total_amount', 'order_time', 'order_status']

    def create(self, validated_data):
        print(validated_data)
        products_data = validated_data.pop('products', [])
        promo_code_data = validated_data.pop('promo_code', None)

        sets_data = validated_data.pop('sets', [])
        if validated_data.get('delivery'):
            delivery_data = validated_data.pop('delivery')
            user_address = UserAddress.objects.get(id=delivery_data['user_address_id'])

        else:
            delivery_data = {}
            user_address = None
        # user = validated_data.pop('user')

        nearest_restaurant = self.context['nearest_restaurant']
        delivery_fee = self.context['delivery_fee']

        with transaction.atomic():
            delivery = Delivery.objects.create(
                restaurant=nearest_restaurant,
                user_address=user_address if user_address else None,
                delivery_time=delivery_data['delivery_time'] if 'delivery_time' in delivery_data else None,
                delivery_fee=delivery_fee
            )

            order = Order.objects.create(
                delivery=delivery,
                # user=user,
                restaurant=nearest_restaurant,
                **validated_data
            )
            if promo_code_data:
                promo_code_instance = PromoCode.objects.filter(code=promo_code_data).first()
                if not promo_code_instance or not promo_code_instance.is_valid():
                    raise serializers.ValidationError({"promo_code": "Промокод недействителен или его срок истек."})
                validated_data['promo_code'] = promo_code_instance
            else:
                validated_data['promo_code'] = None

            for product_data in products_data:
                topping_ids = product_data.pop('topping_ids', [])
                excluded_ingredient_ids = product_data.pop('excluded_ingredient_ids', [])

                order_item = OrderItem(order=order, product_size_id=product_data['product_size_id'],
                                       quantity=product_data['quantity'], is_bonus=product_data['is_bonus'])

                if topping_ids:
                    toppings = Topping.objects.filter(id__in=topping_ids)
                    order_item.save()  # Сохраняем объект перед установкой связей ManyToMany
                    order_item.topping.set(toppings)  # Устанавливаем начинки

                else:
                    order_item.save()
                # if excluded_ingredient_ids:
                #     excluded_ingredients = Ingredient.objects.filter(id__in=excluded_ingredient_ids)
                #     order_item.excluded_ingredient.set(excluded_ingredients)

            # for set_data in sets_data:
            #     set_order_item = OrderItem(order=order, set_id=set_data['set_id'], quantity=set_data['quantity'])
            #     set_order_item.save()

        return order


class ProductOrderItemPreviewSerializer(serializers.Serializer):
    product_size_id = serializers.IntegerField(write_only=True)
    topping_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    excluded_ingredient_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    quantity = serializers.IntegerField()


# class SetOrderItemPreviewSerializer(serializers.Serializer):
#     set_id = serializers.IntegerField(write_only=True)
#     quantity = serializers.IntegerField()


class OrderPreviewSerializer(serializers.Serializer):
    user_address_id = serializers.IntegerField()


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['image', 'description', 'contact_number']


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ['code', 'valid_from', 'valid_to', 'discount', 'active']


class ReOrderToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ['id', 'name', 'price']


class ReOrderProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

    class Meta:
        model = Product
        fields = ['id', 'name', 'image_url', 'description']


class ReOrderProductSizeSerializer(serializers.ModelSerializer):
    product = ReOrderProductSerializer(read_only=True)  # Нудно передать дальше
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2,
                                     read_only=True)  # Если цена прямо не связана с размером и зависит от продукта

    class Meta:
        model = ProductSize
        fields = ['id', 'size', 'product', 'price', 'discounted_price', 'bonus_price']

    def to_representation(self, instance):

        ret = super().to_representation(instance)

        product_size_serializer = ReOrderProductSerializer(instance.product, context=self.context)
        ret['product_size'] = product_size_serializer.data



        return ret


class ReOrderItemSerializer(serializers.ModelSerializer):
    product_size = ReOrderProductSizeSerializer(read_only=True) # Нудно передать дальше
    topping = ReOrderToppingSerializer(many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_size', 'topping', 'quantity', 'total_amount', 'is_bonus']
    def to_representation(self, instance):
        """
        Переопределяем метод to_representation для того, чтобы передать контекст дальше во вложенные сериализаторы.
        """
        # Получаем стандартное представление данных модели
        ret = super().to_representation(instance)

        # Создаем экземпляр сериализатора для product_size с передачей контекста
        product_size_serializer = ReOrderProductSizeSerializer(instance.product_size, context=self.context)
        ret['product_size'] = product_size_serializer.data

        # Создаем экземпляр сериализатора для topping с передачей контекста
        topping_serializer = ReOrderToppingSerializer(instance.topping.all(), many=True, context=self.context)
        ret['topping'] = topping_serializer.data

        return ret

class ReOrderSerializer(serializers.ModelSerializer):
    order_items = ReOrderItemSerializer(many=True, read_only=True) # Нудно передать дальше

    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'delivery', 'order_time', 'total_amount', 'order_items', 'payment_method',
                  'order_status', 'comment']
    def to_representation(self, instance):
        """
        Переопределяем метод to_representation для того, чтобы передать контекст дальше во вложенные сериализаторы.
        """
        # Получаем стандартное представление данных модели
        ret = super().to_representation(instance)

        # Создаем экземпляр сериализатора для order_items с передачей контекста
        order_items_serializer = ReOrderItemSerializer(instance.order_items.all(), many=True, context=self.context)
        ret['order_items'] = order_items_serializer.data

        return ret