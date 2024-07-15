# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from apps.orders.models import Order, Restaurant, Delivery
from .serializers import OrderSerializer
from geopy.distance import geodesic

from ...authentication.models import UserAddress


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user_address = request.data.get('delivery').get('user_address')
        user_address_instance = UserAddress.objects.get(id=user_address)

        if not user_address_instance.latitude or not user_address_instance.longitude:
            return Response({"error": "User address does not have coordinates."}, status=status.HTTP_400_BAD_REQUEST)

        user_location = (user_address_instance.latitude, user_address_instance.longitude)
        nearest_restaurant = None
        min_distance = float('inf')

        for restaurant in Restaurant.objects.all():
            if restaurant.latitude and restaurant.longitude:
                restaurant_location = (restaurant.latitude, restaurant.longitude)
                distance = geodesic(user_location, restaurant_location).kilometers
                if distance < min_distance:
                    min_distance = distance
                    nearest_restaurant = restaurant

        if nearest_restaurant:
            request.data['restaurant'] = nearest_restaurant.id

        return super().create(request, *args, **kwargs)
