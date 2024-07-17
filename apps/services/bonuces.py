from decimal import Decimal

BONUS_PERCENTAGE_MOBILE = 5  # Процент бонусов для мобильных приложений
BONUS_PERCENTAGE_WEB = 3  # Процент бонусов для веб-сайта


def calculate_bonus_points(order_total, delivery_fee, order_source):
    total_order_amount = order_total - delivery_fee
    if order_source == 'mobile':
        bonus_percentage = BONUS_PERCENTAGE_MOBILE
    elif order_source == 'web':
        bonus_percentage = BONUS_PERCENTAGE_WEB
    else:
        bonus_percentage = Decimal('0.0')  # Если источник заказа неизвестен, бонусы не начисляются

    bonus_points = total_order_amount * (bonus_percentage / Decimal('100'))
    return bonus_points


def apply_bonus_points(user, bonus_points):
    if user.bonus is None:
        user.bonus = 0
    user.bonus += bonus_points
    user.save()
