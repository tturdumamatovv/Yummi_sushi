from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from apps.services.get_coordinates import get_coordinates
from .models import Restaurant, Order
from apps.services.bonuces import apply_bonus_points
from apps.services.firebase_notification import send_firebase_notification


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
            # Обновление данных доставки и последнего заказа
            instance.delivery.delivery_time = datetime.now()
            instance.delivery.save()
            instance.user.last_order = datetime.now()
            instance.user.save()
            apply_bonus_points(instance.user, instance.total_bonus_amount)

        # Отправка уведомления через Firebase
        if instance.user.fcm_token:
            try:
                send_firebase_notification(instance.user.fcm_token, "Изменение статуса заказа",
                                           f"Статус вашего заказа {instance.id} изменен на {instance.order_status}")
            except Exception as e:
                print(f"Ошибка при отправке уведомления: {e}")

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "orders_notifications", {
                "type": "send_notification",
                "message": f"Новый заказ №: {instance.id}"
            }
        )
