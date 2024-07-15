def calculate_delivery_fee(distance_km):
    if distance_km <= 3:
        return 150
    elif distance_km <= 4:
        return 160
    elif distance_km <= 5:
        return 170
    elif distance_km <= 6:
        return 190
    elif distance_km <= 7:
        return 210
    elif distance_km <= 8:
        return 220
    elif distance_km <= 9:
        return 230
    elif distance_km <= 10:
        return 250
    elif distance_km <= 11:
        return 270
    elif distance_km <= 12:
        return 320
    elif distance_km <= 13:
        return 350
    elif distance_km <= 14:
        return 370
    elif distance_km <= 15:
        return 380
    else:
        return 380