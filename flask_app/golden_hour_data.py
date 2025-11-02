import datetime
import math

class EventData:
    def __init__(self, json_data : dict):
        self.temp = json_data['main']['temp']
        self.weather = json_data['weather']
        self.visibility = json_data['visibility']

    def calc_golden_score(self):
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
            score += EventData.lerp(0, 25, (self.temp - 30) / (65 - 30))
        elif self.temp > 75:
            score += EventData.lerp(0, 25, (100 - self.temp) / (100 - 75))

        return math.floor(score / 75 * 100)

    @staticmethod
    def lerp(v0, v1, t):
        return v0 + t * (v1 - v0)

    def get_image_name(self):
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
    def __init__(self, date : int, timezone : int, sunrise_data: dict, sunset_data: dict):
        self.date = self.format_timestamp(date, timezone)
        self.sunrise_event = None
        self.sunset_event = None
    
        if sunrise_data != None:
            self.sunrise_event = EventData(sunrise_data)
    
        if sunset_data != None:
            self.sunset_event = EventData(sunset_data)

    def format_timestamp(self, timestamp, timezone_offset):
        '''
        Convert a UTC timestamp to local time based on timezone offset.
        Returns formatted time string "HH:MM:SS".
        '''

        local_timezone = datetime.timezone(datetime.timedelta(seconds=timezone_offset))

        utc_dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        local_dt = utc_dt.astimezone(local_timezone)

        formatted_time = local_dt.strftime("%m/%d/%Y")

        return formatted_time

class GoldenHourData:
    def __init__(self, json_data : dict):
        self.city_name = json_data['city']['name']
        self.coordinates = (json_data['city']['coord']['lat'], json_data['city']['coord']['lon'])
        self.country = json_data['city']['country']
        self.timezone = json_data['city']['timezone']
        self.sunrise = json_data['city']['sunrise']
        self.sunset = json_data['city']['sunset']
        self.sunrise_dt = self.format_timestamp(self.sunrise)
        self.sunset_dt = self.format_timestamp(self.sunset)
        self.days = []

        date = json_data['list'][0]['dt']
        sunrise_hour = self.sunrise - (self.sunrise % 3600)
        sunset_hour = self.sunset - (self.sunset % 3600)

        while True:
            sunrise = list(filter(lambda x: x['dt'] == sunrise_hour, json_data['list']))
            if len(sunrise) == 0:
                sunrise = None
            else:
                sunrise = sunrise[0]
            

            sunset = list(filter(lambda x: x['dt'] == sunset_hour, json_data['list']))
            if len(sunset) == 0:
                sunset = None
            else:
                sunset = sunset[0]

            if sunrise == None and sunset == None and len(self.days) > 0:
                break

            self.days.append(Day(date, self.timezone, sunrise, sunset))
            sunrise_hour += 86400
            sunset_hour += 86400
            date += 86400

    def format_timestamp(self, timestamp):
        '''
        Convert a UTC timestamp to local time based on timezone offset.
        Returns formatted time string "HH:MM:SS".
        '''

        local_timezone = datetime.timezone(datetime.timedelta(seconds=self.timezone))

        utc_dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        local_dt = utc_dt.astimezone(local_timezone)
        
        formatted_time = local_dt.strftime("%H:%M:%S")

        return formatted_time