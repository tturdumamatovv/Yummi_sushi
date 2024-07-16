from datetime import datetime


def is_restaurant_open(restaurant, order_time):
    if restaurant.opening_hours:
        opening_hours = restaurant.opening_hours.split('-')
        if len(opening_hours) == 2:
            opening_time = datetime.strptime(opening_hours[0], '%H:%M').time()
            closing_time = datetime.strptime(opening_hours[1], '%H:%M').time()
            if opening_time <= order_time.time() <= closing_time:
                return True
    return False