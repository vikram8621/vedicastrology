from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder


def get_location(place_name):
    geolocator = Nominatim(user_agent="vedic_app")

    location = geolocator.geocode(place_name)

    if not location:
        raise ValueError("Place not found")

    lat = location.latitude
    lon = location.longitude

    tf = TimezoneFinder()

    timezone = tf.timezone_at(
        lat=lat,
        lng=lon
    )

    return lat, lon, timezone