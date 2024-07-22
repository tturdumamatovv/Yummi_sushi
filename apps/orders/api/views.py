# views.py
from datetime import datetime
from decimal import Decimal

from apps.authentication.models import UserAddress
from apps.orders.models import Restaurant, TelegramBotToken, Report
from apps.services.calculate_delivery_fee import calculate_delivery_fee
from apps.services.calculate_distance import get_distance_between_locations
from apps.services.generate_message import generate_order_message
from apps.services.is_restaurant_open import is_restaurant_open
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import OrderSerializer, OrderPreviewSerializer, ReportSerializer
from ...product.models import ProductSize, Set, Topping, Ingredient
from ...services.bonuces import calculate_bonus_points, apply_bonus_points
from ...services.calculate_bonus import calculate_and_apply_bonus

from telegram import Bot
from asgiref.sync import async_to_sync


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        user_address_id = request.data.get('delivery').get('user_address_id')
        is_pickup = request.data.get('is_pickup', False)
        restaurant_id = request.data.get('restaurant_id', None)
        order_source = request.data.get('order_source', 'unknown')
        order_time = datetime.now()
        user_address_instance = UserAddress.objects.get(id=user_address_id, user=user)

        if not is_pickup and (not user_address_instance.latitude or not user_address_instance.longitude):
            return Response({"error": "User address does not have coordinates."}, status=status.HTTP_400_BAD_REQUEST)

        if not is_pickup:
            user_location = (user_address_instance.latitude, user_address_instance.longitude)
            nearest_restaurant = None
            min_distance = float('inf')

            for restaurant in Restaurant.objects.all():
                if restaurant.latitude and restaurant.longitude:
                    restaurant_location = (restaurant.latitude, restaurant.longitude)
                    distance = get_distance_between_locations('AIzaSyCWbO5aOn8hS3EWJycj73dHqH8fHHfO4w4', user_location, restaurant_location)
                    if distance is not None and distance < min_distance and is_restaurant_open(restaurant, order_time):
                        min_distance = distance
                        nearest_restaurant = restaurant

            if not nearest_restaurant:
                return Response({"error": "No available restaurants found or all are closed."},
                                status=status.HTTP_400_BAD_REQUEST)

            delivery_fee = calculate_delivery_fee(min_distance)
        else:
            if restaurant_id:
                try:
                    nearest_restaurant = Restaurant.objects.get(id=restaurant_id)
                    if not is_restaurant_open(nearest_restaurant, order_time):
                        return Response({"error": "Selected restaurant is closed."}, status=status.HTTP_400_BAD_REQUEST)
                except Restaurant.DoesNotExist:
                    return Response({"error": "Restaurant not found."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Restaurant ID is required for pickup."}, status=status.HTTP_400_BAD_REQUEST)

            min_distance = 0
            delivery_fee = 0

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.context['nearest_restaurant'] = nearest_restaurant
        serializer.context['delivery_fee'] = delivery_fee
        serializer.context['user'] = user

        self.perform_create(serializer)

        order = serializer.instance
        try:
            total_order_amount = calculate_and_apply_bonus(order)
            order.total_amount = total_order_amount + delivery_fee
            order.save()
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        bonus_points = calculate_bonus_points(Decimal(order.total_amount), Decimal(delivery_fee), order_source)
        apply_bonus_points(user, bonus_points)

        message = generate_order_message(order, min_distance, delivery_fee)
        print(message)
        bot_token_instance = TelegramBotToken.objects.first()
        if bot_token_instance:
            telegram_bot_token = bot_token_instance.bot_token
            telegram_chat_ids = nearest_restaurant.get_telegram_chat_ids()
            bot = Bot(token=telegram_bot_token)
            for chat_id in telegram_chat_ids:
                async_to_sync(bot.send_message)(chat_id=chat_id, text=message)
        else:
            return Response({"error": "Не установлен токен бота Telegram."}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderPreviewView(generics.GenericAPIView):
    serializer_class = OrderPreviewSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        order_time = datetime.now()
        user_address_id = data.get('user_address_id')
        is_pickup = data.get('is_pickup', False)

        try:
            user_address_instance = UserAddress.objects.get(id=user_address_id, user=user)
        except UserAddress.DoesNotExist:
            return Response({"error": "User address does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if not is_pickup and (not user_address_instance.latitude or not user_address_instance.longitude):
            return Response({"error": "User address does not have coordinates."}, status=status.HTTP_400_BAD_REQUEST)

        nearest_restaurant = None
        min_distance = float('inf')
        delivery_fee = 0

        if not is_pickup:
            user_location = (user_address_instance.latitude, user_address_instance.longitude)

            for restaurant in Restaurant.objects.all():
                if restaurant.latitude and restaurant.longitude:
                    restaurant_location = (restaurant.latitude, restaurant.longitude)
                    distance = get_distance_between_locations('AIzaSyCWbO5aOn8hS3EWJycj73dHqH8fHHfO4w4', user_location,
                                                              restaurant_location)
                    if distance is not None and distance < min_distance and is_restaurant_open(restaurant, order_time):
                        min_distance = distance
                        nearest_restaurant = restaurant

            if not nearest_restaurant:
                return Response({"error": "No available restaurants found or all are closed."},
                                status=status.HTTP_400_BAD_REQUEST)

            delivery_fee = calculate_delivery_fee(min_distance)
        else:
            nearest_restaurant = Restaurant.objects.first()  # Use the default restaurant for pickup

        total_amount = 0
        products_data = data.get('products', [])
        sets_data = data.get('sets', [])

        order_items_details = []

        for product_data in products_data:
            product_size_id = product_data.get('product_size_id')
            topping_ids = product_data.get('topping_ids', [])
            excluded_ingredient_ids = product_data.get('excluded_ingredient_ids', [])
            quantity = product_data.get('quantity', 1)

            try:
                product_size = ProductSize.objects.get(id=product_size_id)
                item_total = product_size.get_price() * quantity
                total_amount += item_total
                order_items_details.append({
                    "product": product_size.product.name,
                    "size": product_size.size.name,
                    "quantity": quantity,
                    "toppings": [topping.name for topping in Topping.objects.filter(id__in=topping_ids)],
                    "excluded_ingredients": [ingredient.name for ingredient in
                                             Ingredient.objects.filter(id__in=excluded_ingredient_ids)],
                    "total": item_total
                })
            except ProductSize.DoesNotExist:
                return Response({"error": f"Product size with id {product_size_id} does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)

        for set_data in sets_data:
            set_id = set_data.get('set_id')
            quantity = set_data.get('quantity', 1)

            try:
                set_item = Set.objects.get(id=set_id)
                item_total = set_item.get_price() * quantity
                total_amount += item_total
                order_items_details.append({
                    "set": set_item.name,
                    "quantity": quantity,
                    "total": item_total
                })
            except Set.DoesNotExist:
                return Response({"error": f"Set with id {set_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            "user": user.full_name,
            "phone_number": user.phone_number,
            "restaurant": nearest_restaurant.name if nearest_restaurant else None,
            "address": {
                "city": user_address_instance.city,
                "street": user_address_instance.street,
                "house_number": user_address_instance.house_number,
                "apartment_number": user_address_instance.apartment_number,
                "entrance": user_address_instance.entrance,
                "floor": user_address_instance.floor,
                "intercom": user_address_instance.intercom,
                "comment": user_address_instance.comment
            } if not is_pickup else "Самовывоз",
            "delivery_info": {
                "distance_km": min_distance,
                "delivery_fee": delivery_fee
            } if not is_pickup else None,
            "payment_info": {
                "method": data.get('payment_method'),
            },
            "total_amount": total_amount + delivery_fee,
            "order_items": order_items_details
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ReportCreateView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        self.send_report_to_telegram(instance)

    def send_report_to_telegram(report):
        try:
            token_instance = TelegramBotToken.objects.get(pk=1)
            bot = Bot(token=token_instance.bot_token)
            channels = token_instance.report_channels.split(',')
            message = f"Новый репорт:\nОписание: {report.description}\nКонтактный номер: {report.contact_number}"

            for chat_id in channels:
                bot.send_message(chat_id=chat_id.strip(), text=message)
                if report.image:
                    image_path = report.image.path
                    bot.send_photo(chat_id=chat_id.strip(), photo=open(image_path, 'rb'))
        except TelegramBotToken.DoesNotExist:
            print("Токен бота Telegram не настроен.")