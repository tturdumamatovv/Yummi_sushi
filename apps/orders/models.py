from django.db import models


# Create your models here.

class Restaurant(models.Model):
    pass

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"


class Delivery(models.Model):
    pass

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"


class Order(models.Model):
    pass

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
