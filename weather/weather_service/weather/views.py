from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
import os, requests, json
import arrow
from django.core.cache import cache

load_dotenv()

API_URL = os.getenv("API_URL")
TIDE_KEY = os.getenv("TIDE_KEY")  
TIDE_CACHE_KEY = os.getenv("TIDE_CACHE_KEY")
WEATHER_CACHE_KEY = os.getenv("WEATHER_CACHE_KEY")

@api_view(["GET"])
def get_locations_weather(request):
    cache_key = WEATHER_CACHE_KEY
    cache_time = 21600
    data = cache.get(cache_key)

    if not data:
        raw_data = requests.get(API_URL)
        decoded_strings = [part.decode('utf-8') for part in raw_data]

        json_str = ''.join(decoded_strings)

        data = json.loads(json_str)
        cache.set(cache_key, data, cache_time)

    return Response(data)


@api_view(["GET"])
def get_tide_forecast(request):
    cache_key = TIDE_CACHE_KEY
    cache_time = 21600
    data = cache.get(cache_key)
    
    if not data:
        
        start = arrow.now().floor('day')
        end = arrow.now().shift(days=1).floor('day')

        response = requests.get(
        'https://api.stormglass.io/v2/tide/extremes/point',
        params={
            'lat': -22.6833,
            'lng': 14.5333,
            'start': start.to('UTC').timestamp(),  # Convert to UTC timestamp
            'end': end.to('UTC').timestamp(),  # Convert to UTC timestamp
        },
        headers={
            'Authorization': TIDE_KEY
        }
        )

        # Do something with response data.
        data = response.json()["data"]
        cache.set(cache_key, data, cache_time)
        
    return Response(data=data)
