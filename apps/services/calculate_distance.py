import googlemaps


def get_distance_between_locations(api_key, origin, destination):
    """
    Calculate the distance between two locations using Google Maps Distance Matrix API.

    :param api_key: Google Maps API key as a string
    :param origin: Tuple containing latitude and longitude of the origin (lat, lon)
    :param destination: Tuple containing latitude and longitude of the destination (lat, lon)
    :return: Distance in kilometers or None if the distance couldn't be calculated
    """
    gmaps = googlemaps.Client(key=api_key)
    result = gmaps.distance_matrix(origins=[origin], destinations=[destination], mode="driving")

    if result['rows'][0]['elements'][0]['status'] == 'OK':
        distance_km = result['rows'][0]['elements'][0]['distance']['value'] / 1000  # distance in kilometers
        return distance_km
    else:
        return None


if __name__ == "__main__":
    api_key = ""
    origin = (42.837155, 74.590484)  # New York City (latitude, longitude)
    destination = (42.843516, 74.588999)  # Los Angeles (latitude, longitude)
    distance = get_distance_between_locations(api_key, origin, destination)
    if distance is not None:
        print(f"The distance between the locations is {distance:.2f} km")
    else:
        print("Could not calculate the distance between the locations")
