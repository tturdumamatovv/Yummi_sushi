from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Restaurant, Order
from apps.services.get_coordinates import get_coordinates
from ..services.bonuces import calculate_bonus_points, apply_bonus_points


@receiver(pre_save, sender=Restaurant)
def set_coordinates(sender, instance, **kwargs):
    if instance.address and (instance.latitude is None or instance.longitude is None):
        latitude, longitude = get_coordinates(instance.address)
        if latitude and longitude:
            instance.latitude = latitude
            instance.longitude = longitude
            instance.save()


@receiver(pre_save, sender=Order)
def check_status_change(sender, instance, **kwargs):
    if instance.pk:
        old_order = sender.objects.get(pk=instance.pk)
        if old_order.order_status != instance.order_status and instance.order_status == 'completed':
            apply_bonus_points(instance.user, instance.total_bonus_amount)


