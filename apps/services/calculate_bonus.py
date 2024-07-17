# services/bonus_products.py
from decimal import Decimal

from apps.orders.models import OrderItem
from apps.product.models import Ingredient, Topping


def calculate_and_apply_bonus(user, order, products_data, sets_data):
    total_order_amount = Decimal('0.00')
    total_bonus_amount = Decimal('0.00')

    for product_data in products_data:
        topping_ids = product_data.pop('topping_ids', [])
        excluded_ingredient_ids = product_data.pop('excluded_ingredient_ids', [])

        is_bonus = product_data.get('is_bonus', False)
        order_item = OrderItem(order=order, product_size_id=product_data['product_size_id'], quantity=product_data['quantity'], is_bonus=is_bonus)
        order_item.save()

        if topping_ids:
            toppings = Topping.objects.filter(id__in=topping_ids)
            order_item.topping.set(toppings)

        if excluded_ingredient_ids:
            excluded_ingredients = Ingredient.objects.filter(id__in=excluded_ingredient_ids)
            order_item.excluded_ingredient.set(excluded_ingredients)

        order_item.total_amount = order_item.calculate_total_amount()
        order_item.save()

        if is_bonus:
            total_bonus_amount += order_item.total_amount
        else:
            total_order_amount += order_item.total_amount

    for set_data in sets_data:
        set_order_item = OrderItem(order=order, set_id=set_data['set_id'], quantity=set_data['quantity'])
        set_order_item.save()
        total_order_amount += set_order_item.calculate_total_amount()
        set_order_item.save()

    order.total_amount = total_order_amount
    order.save()

    if user.bonus >= total_bonus_amount:
        user.bonus -= total_bonus_amount
        user.save()
    else:
        raise ValueError("Not enough bonus points.")

    return total_order_amount
