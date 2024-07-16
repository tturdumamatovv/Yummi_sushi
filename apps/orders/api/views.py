# views.py
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from apps.authentication.models import UserAddress
from apps.orders.models import Restaurant
from apps.services.calculate_delivery_fee import calculate_delivery_fee
from apps.services.calculate_distance import get_distance_between_locations
from .serializers import OrderSerializer
from ...services.generate_message import generate_order_message


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        user_address_id = request.data.get('delivery').get('user_address_id')
        user_address_instance = UserAddress.objects.get(id=user_address_id, user=user)

        if not user_address_instance.latitude or not user_address_instance.longitude:
            return Response({"error": "User address does not have coordinates."}, status=status.HTTP_400_BAD_REQUEST)

        user_location = (user_address_instance.latitude, user_address_instance.longitude)
        nearest_restaurant = None
        min_distance = float('inf')

        for restaurant in Restaurant.objects.all():
            if restaurant.latitude and restaurant.longitude:
                restaurant_location = (restaurant.latitude, restaurant.longitude)
                distance = get_distance_between_locations('AIzaSyCWbO5aOn8hS3EWJycj73dHqH8fHHfO4w4', user_location, restaurant_location)
                if distance is not None and distance < min_distance:
                    min_distance = distance
                    nearest_restaurant = restaurant

        if nearest_restaurant:
            delivery_fee = calculate_delivery_fee(min_distance)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.context['nearest_restaurant'] = nearest_restaurant
            serializer.context['delivery_fee'] = delivery_fee
            serializer.context['user'] = user

            self.perform_create(serializer)

            order = serializer.instance

            # Формирование сообщения для Telegram
            message = generate_order_message(order, min_distance, delivery_fee)
            print(message)

            # Отправка сообщения в Telegram
            # send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": "No available restaurants found."}, status=status.HTTP_400_BAD_REQUEST)