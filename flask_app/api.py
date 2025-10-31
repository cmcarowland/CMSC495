from golden_hour_data import GoldenHourData, Day, EventData

import requests
import datetime
import os

API_URL = f'http://api.openweathermap.org/'
PRO_URL = 'https://pro.openweathermap.org/'
GEO_ENDPOINT = 'geo/1.0/direct?q='
REVERSE_GEO_ENDPOINT = 'geo/1.0/reverse?'
WEATHER_ENDPOINT = 'data/2.5/weather?'
HOURLY_ENDPOINT = 'data/2.5/forecast/hourly?'
OPENMAP_API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY")

def query_location(city, state, country):
    '''
    Query location data from OpenWeatherMap Geocoding API.
    Returns a list of location data dictionaries or None if not found.
    '''

    url = f'{API_URL}{GEO_ENDPOINT}'
    if city:
        url += f'{city}'
    if state:
        url += f',{state}'
    if country:
        url += f',{country}'

    url += f'&limit=1&appid={OPENMAP_API_KEY}'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    data = response.json()
    if data is None or len(data) == 0:
        return None

    return data

def format_timestamp(timestamp, timezone_offset):
    '''
    Convert a UTC timestamp to local time based on timezone offset.
    Returns formatted time string "HH:MM:SS".
    '''

    local_timezone = datetime.timezone(datetime.timedelta(seconds=timezone_offset))

    utc_dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
    local_dt = utc_dt.astimezone(local_timezone)
    
    formatted_time = local_dt.strftime("%H:%M:%S")

    return formatted_time

def query_current_weather(latitude, longitude):
    '''
    Query current weather data from OpenWeatherMap API.
    Returns a dictionary with weather data or None if not found.
    '''

    url = f'{API_URL}{WEATHER_ENDPOINT}' \
        f'lat={latitude}&lon={longitude}&units=Imperial' \
        f'&appid={OPENMAP_API_KEY}'
    
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    weather_data = response.json()
    if weather_data is None:
        return None

    weather_data['sys']['sunrise_dt'] = format_timestamp(weather_data['sys']['sunrise'], weather_data['timezone'])
    weather_data['sys']['sunset_dt'] = format_timestamp(weather_data['sys']['sunset'], weather_data['timezone'])
    
    return weather_data

def query_hourly_forecast(latitude, longitude):
    '''
    Query hourly weather forecast data from OpenWeatherMap Pro API.
    Returns a dictionary with forecast data or None if not found.
    '''
    
    url = f'{PRO_URL}{HOURLY_ENDPOINT}' \
        f'lat={latitude}&lon={longitude}&units=Imperial' \
        f'&appid={OPENMAP_API_KEY}'
    
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    # print(response.json())
    ghd = GoldenHourData(response.json())
    
    return ghd

def get_city_name(latitude, longitude):
    '''
    Get city name from latitude and longitude using OpenWeatherMap Reverse Geocoding API.
    Returns city name string or None if not found.
    '''

    url = f'{API_URL}{REVERSE_GEO_ENDPOINT}' \
        f'lat={latitude}&lon={longitude}&limit=1&appid={OPENMAP_API_KEY}'

    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()
    if data is None or len(data) == 0:
        return None

    return data[0].get('name', 'Unknown')