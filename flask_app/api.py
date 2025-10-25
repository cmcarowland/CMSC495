import requests
import datetime
import os

API_URL = f'http://api.openweathermap.org/'
GEO_ENDPOINT = 'geo/1.0/direct?q='
WEATHER_ENDPOINT = 'data/2.5/weather?'
OPENMAP_API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY")

def query_location(city, state, country):
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
    local_timezone = datetime.timezone(datetime.timedelta(seconds=timezone_offset))

    utc_dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
    local_dt = utc_dt.astimezone(local_timezone)
    
    formatted_time = local_dt.strftime("%H:%M:%S")

    return formatted_time

def query_weather(latitude, longitude):
    url = f'{API_URL}{WEATHER_ENDPOINT}' \
        f'lat={latitude}&lon={longitude}&units=Imperial' \
        f'&appid={OPENMAP_API_KEY}'
    
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    weather_data = response.json()
    print(weather_data)
    weather_data['sys']['sunrise'] = format_timestamp(weather_data['sys']['sunrise'], weather_data['timezone'])
    weather_data['sys']['sunset'] = format_timestamp(weather_data['sys']['sunset'], weather_data['timezone'])
    
    return weather_data