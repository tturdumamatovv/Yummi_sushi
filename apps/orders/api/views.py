# views.py
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from apps.authentication.models import UserAddress
from apps.orders.models import Restaurant
from apps.services.calculate_delivery_fee import calculate_delivery_fee
from apps.services.calculate_distance import get_distance_between_locations
from .serializers import OrderSerializer


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        user_address_id = request.data.get('delivery').get('user_address')
        user_address_instance = UserAddress.objects.get(id=user_address_id, user=user)

        if not user_address_instance.latitude or not user_address_instance.longitude:
            return Response({"error": "User address does not have coordinates."}, status=status.HTTP_400_BAD_REQUEST)

        user_location = (user_address_instance.latitude, user_address_instance.longitude)
        nearest_restaurant = None
        min_distance = float('inf')

        for restaurant in Restaurant.objects.all():
            if restaurant.latitude and restaurant.longitude:
                restaurant_location = (restaurant.latitude, restaurant.longitude)
                distance = get_distance_between_locations(user_location, restaurant_location)
                if distance is not None and distance < min_distance:
                    min_distance = distance
                    nearest_restaurant = restaurant

        if nearest_restaurant:
            delivery_fee = calculate_delivery_fee(min_distance)
            delivery_data = request.data.get('delivery')
            delivery_data['restaurant'] = nearest_restaurant.id
            delivery_data['delivery_fee'] = delivery_fee
            request.data['restaurant'] = nearest_restaurant.id
            request.data['delivery']['delivery_fee'] = delivery_fee
            request.data['user'] = user.id
            request.data['total_amount'] = 0  # This will be calculated later in the save method

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": "No available restaurants found."}, status=status.HTTP_400_BAD_REQUEST)