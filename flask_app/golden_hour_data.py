'''
Golden Hour App Group 1
UMGC CMSC 495 7385
Shivam Patel, Raymond Rowland, Mariam Ahmed, Katrina Wilhelm, Paul Cooper
November 5, 2025

golden_hour_data.py

Defines data structures for Golden Hour weather data processing.
Contains classes: GoldenHourData, Day, EventData.
'''

from flask_app import api

import datetime
import math

class EventData:
    """
    Represents weather event data and computes a 'golden score'
    based on temperature, weather conditions, and visibility.

    Also includes helper methods for linear interpolation and
    determining the appropriate weather icon name.
    """
    def __init__(self, json_data : dict):
        """
        Initialize the EventData object with JSON weather data.

        Args:
            json_data (dict): A dictionary containing weather data
                with keys like 'main', 'weather', and optionally 'visibility'.
        """
        self.temp = json_data['main']['temp']
        self.weather = json_data['weather']
        self.visibility = json_data.get('visibility', 10000)

    def calc_golden_score(self):
        """
        Calculate a 'golden score' (0 - 100) representing ideal conditions.

        The score is determined by:
          - Weather conditions (clear or partly cloudy)
          - Visibility range
          - Temperature closeness to the 65 - 75°F comfort range

        Returns:
            int: A score between 0 and 100, where higher values indicate better conditions.
        """
        score = 0
        
        weather_id = self.weather[0]['id']
        if weather_id == 800:
            score += 25
        elif 801 <= weather_id <= 803:
            score += (804 - weather_id) * 5

        if self.visibility >= 5000:
            score += 25
        else:
            score += EventData.lerp(0, 25, self.visibility / 5000)

        if 65 <= self.temp <= 75:
            score += 25
        elif self.temp < 65:
            score += EventData.lerp(0, 25, (self.temp - 40) / 25)
        elif self.temp > 75:
            score += EventData.lerp(0, 25, (100 - self.temp) / 25)

        return math.floor(score / 75 * 100)

    @staticmethod
    def lerp(v0, v1, t):
        """
        Perform linear interpolation between two values.

        Args:
            v0 (float): Start value.
            v1 (float): End value.
            t (float): Interpolation factor (0.0 - 1.0).

        Returns:
            float: The interpolated value between v0 and v1.
        """
        if t < 0:
            return v0
        if t > 1:
            return v1

        return v0 + t * (v1 - v0)

    def get_image_name(self):
        """
        Map the weather condition ID to a descriptive image name.

        Uses the OpenWeatherMap weather ID convention to determine
        the appropriate icon name (e.g., 'clear-day', 'rain', 'fog').

        Returns:
            str: The name of the weather image/icon.
        """
        weather_id = self.weather[0]['id']
        # if (weather_data['dt'] < weather_data['sys']['sunrise'] or
        #     weather_data['dt'] > weather_data['sys']['sunset']):
        #     weather_id += 1000

        if weather_id - 200 < 100:
            return "thunderstorm"
        
        if weather_id - 300 < 100:
            return "drizzle"
        
        if weather_id == 500:
            return "light-rain"
        elif weather_id == 504:
            return "extreme-rain"
        elif weather_id == 511:
            return "sleet"
        elif weather_id - 500 < 100:
            return "rain"
        
        if 611 <= weather_id <= 613:
            return "sleet"
        elif weather_id - 600 < 100:
            return "snow"
        
        if weather_id - 700 < 100:
            return "fog"
        
        if weather_id == 800:
            return "clear-day"
        
        if 801 <= weather_id <= 803:
            return "partly-cloudy-day"
        elif weather_id - 800 < 100:
            return "cloudy"
        
        # night icons
        if weather_id == 1800:
            return "clear-night"
        if 1801 <= weather_id <= 1803:
            return "partly-cloudy-night"
        elif weather_id == 1804:
            return "cloudy"

        return "unknown"

class Day:
    """
    Represents a single calendar day containing sunrise and sunset
    weather event data. It formats a given timestamp into a readable
    date and initializes EventData objects for each event.
    """
    def __init__(self, date : int, timezone : int, sunrise_data: dict, sunset_data: dict):
        """
        Initialize the Day object.

        Args:
            date (int): The UTC timestamp for the date.
            timezone (int): The timezone offset in seconds from UTC.
            sunrise_data (dict): JSON data for the sunrise event.
            sunset_data (dict): JSON data for the sunset event.
        """
        self.date = self.format_timestamp_as_M_D_Y(date, timezone)
        self.sunrise_event = None
        self.sunset_event = None
    
        if sunrise_data != None:
            self.sunrise_event = EventData(sunrise_data)
    
        if sunset_data != None:
            self.sunset_event = EventData(sunset_data)

    def format_timestamp_as_M_D_Y(self, timestamp, timezone_offset):
        """
        Convert a UTC timestamp to local time based on timezone offset.

        Args:
            timestamp (int): UTC timestamp in seconds.
            timezone_offset (int): Offset from UTC in seconds (can be negative).

        Returns:
            str: Formatted local date string in the format "MM/DD/YYYY".
        """

        local_timezone = datetime.timezone(datetime.timedelta(seconds=timezone_offset))

        utc_dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        local_dt = utc_dt.astimezone(local_timezone)

        formatted_time = local_dt.strftime("%m/%d/%Y")

        return formatted_time

class GoldenHourData:
    """
    Represents golden hour (sunrise and sunset) data for a specific city.

    Parses JSON data containing forecast information, converts timestamps
    to readable formats, and builds a list of Day objects containing
    sunrise and sunset event data.
    """
    def __init__(self, json_data : dict):
        """
        Initialize the GoldenHourData object.

        Args:
            json_data (dict): The JSON data structure from the weather API,
                containing city info and hourly forecast list.
        """
 
        self.city_name = json_data['city']['name']
        if 'lat' in json_data['city']['coord']:
            self.coordinates = (json_data['city']['coord']['lat'], json_data['city']['coord']['lon'])
        else:
            self.coordinates = (0, 0)

        self.country = json_data['city']['country']
        self.timezone = json_data['city']['timezone']
        self.sunrise = json_data['city']['sunrise']
        self.sunset = json_data['city']['sunset']
        self.sunrise_dt = self.format_timestamp_as_H_M_S(self.sunrise)
        self.sunset_dt = self.format_timestamp_as_H_M_S(self.sunset)
        self.days = []

        date = json_data['list'][0]['dt']
        sunrise_hour = self.sunrise - (self.sunrise % 3600)
        sunset_hour = self.sunset - (self.sunset % 3600)

        while True:
            sunrise = next(filter(lambda x: x['dt'] == sunrise_hour, json_data['list']), None)
            if sunrise_hour < datetime.datetime.now().timestamp() and sunrise is None:
                data = api.query_historical_forecast(self.coordinates[0], self.coordinates[1], sunrise_hour)
                sunrise = data
            
            sunset = next(filter(lambda x: x['dt'] == sunset_hour, json_data['list']), None)
            if sunset_hour < datetime.datetime.now().timestamp() and sunset is None:
                data = api.query_historical_forecast(self.coordinates[0], self.coordinates[1], sunset_hour)
                sunset = data

            if sunrise == None and sunset == None and len(self.days) > 0:
                break

            self.days.append(Day(date, self.timezone, sunrise, sunset))
            sunrise_hour += 86400
            sunset_hour += 86400
            date += 86400

    def format_timestamp_as_H_M_S(self, timestamp):
        """
        Convert a UTC timestamp to local time based on the timezone offset.

        Args:
            timestamp (int): UTC timestamp in seconds.

        Returns:
            str: Formatted local time string in the format "HH:MM:SS".
        """

        local_timezone = datetime.timezone(datetime.timedelta(seconds=self.timezone))

        utc_dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        local_dt = utc_dt.astimezone(local_timezone)
        
        formatted_time = local_dt.strftime("%I:%M:%S %p")

        return formatted_time