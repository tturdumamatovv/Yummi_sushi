from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import UserAddress
from ..services.get_coordinates import get_coordinates


@receiver(pre_save, sender=UserAddress)
def set_coordinates(sender, instance, **kwargs):
    if instance.city and instance.street and instance.house_number and (
            instance.latitude is None or instance.longitude is None):
        address = f"{instance.city}, {instance.street} {instance.house_number}"
        latitude, longitude = get_coordinates(address)
        if latitude and longitude:
            instance.latitude = latitude
            instance.longitude = longitude
