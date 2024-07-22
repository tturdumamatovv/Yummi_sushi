from decimal import Decimal

from apps.orders.models import PercentCashback

percents = PercentCashback.objects.get(id=1)
if not percents:
    percents = PercentCashback.objects.create(mobile_percelnt=5, web_percelnt=3)

BONUS_PERCENTAGE_MOBILE = percents.mobile_percelnt
BONUS_PERCENTAGE_WEB = percents.web_percent


def calculate_bonus_points(order_total, delivery_fee, order_source):
    total_order_amount = order_total - delivery_fee
    if order_source == 'mobile':
        bonus_percentage = BONUS_PERCENTAGE_MOBILE
    elif order_source == 'web':
        bonus_percentage = BONUS_PERCENTAGE_WEB
    else:
        bonus_percentage = Decimal('0.0')

    bonus_points = total_order_amount * (bonus_percentage / Decimal('100'))
    return bonus_points


def apply_bonus_points(user, bonus_points):
    if user.bonus is None:
        user.bonus = 0
    user.bonus += bonus_points
    user.save()
