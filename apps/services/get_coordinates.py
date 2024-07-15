import requests


def get_coordinates(address):
    base_url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json',
        'addressdetails': 1,
        'limit': 1
    }
    headers = {
        'User-Agent': 'YourAppName (your-email@example.com)'
    }
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()

        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        results = response.json()
        if results:
            location = results[0]
            return float(location['lat']), float(location['lon'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")
    except ValueError as e:
        print(f"Error decoding JSON response: {e}")
    return None, None
