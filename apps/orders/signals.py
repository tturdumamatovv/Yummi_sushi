from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Restaurant
from apps.services.get_coordinates import get_coordinates


@receiver(pre_save, sender=Restaurant)
def set_coordinates(sender, instance, **kwargs):
    if instance.address and (instance.latitude is None or instance.longitude is None):
        latitude, longitude = get_coordinates(instance.address)
        if latitude and longitude:
            instance.latitude = latitude
            instance.longitude = longitude
            instance.save()
