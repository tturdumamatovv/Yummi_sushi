def generate_order_message(order, delivery_distance_km, delivery_fee):
    message = (
        f"Новый заказ #{order.id}\n"
        f"Пользователь: {order.user}\n"
        f"Ресторан: {order.restaurant.name}\n"
        f"Адрес доставки: {order.delivery.user_address}\n"
        f"Статус: {order.get_order_status_display()}\n"

        "Детали заказа:\n"
        "=================\n"

    )

    for item in order.order_items.all():
        if item.product_size:
            item_details = f"Продукт: {item.product_size.product.name} ({item.product_size.size.name})\n"
            item_details += f"Количество: {item.quantity}\n"
            item_details += f"Сумма: {item.total_amount}\n"

        if item.set:
            item_details = f"Сет: {item.set.name}\n"
            item_details += f"Количество: {item.quantity}\n"
            item_details += f"Сумма: {item.total_amount}\n"

        if item.topping.exists():
            item_details += "Топинги:\n"
            for topping in item.topping.all():
                item_details += f" - {topping.name}\n"

        if item.excluded_ingredient.exists():
            item_details += "Исключенные ингредиенты:\n"
            for ingredient in item.excluded_ingredient.all():
                item_details += f" - {ingredient.name}\n"

        message += item_details + "----------------\n"

    message += (
        f"Растояние доставки: {delivery_distance_km:.2f} км\n"
        f"Стоимость доставки: {delivery_fee} сом\n\n"
        f"Общая сумма: {order.total_amount}\n"
    )

    return message
