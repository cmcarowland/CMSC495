'''
Golden Hour App Group 1
UMGC CMSC 495 7385
Shivam Patel, Raymond Rowland, Mariam Ahmed, Katrina Wilhelm, Paul Cooper
November 20, 2025

test_unit_eventdata.py

Unit tests for the EventData class.
Tests various conditions and scoring calculations.
'''

from flask_app.golden_hour_data import EventData

def test_event_score():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 
        'visibility': 10000, 
    }
    event_data = EventData(json_data)
    assert event_data.calc_golden_score() == 100

def test_event_score_partial_conditions():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 801, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 
        'visibility': 10000, 
    }
    event_data = EventData(json_data)
    assert event_data.calc_golden_score() == 86

def test_event_score_mostly_conditions():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 802, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 
        'visibility': 10000, 
    }
    event_data = EventData(json_data)
    assert event_data.calc_golden_score() == 80

def test_event_score_cloudy_conditions():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 803, 'main': 'Cloudy', 'description': 'overcast clouds', 'icon': '04d'}], 
        'visibility': 10000, 
    }
    event_data = EventData(json_data)
    assert event_data.calc_golden_score() == 73

def test_event_score_overcast_conditions():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 804, 'main': 'Overcast', 'description': 'overcast clouds', 'icon': '04d'}], 
        'visibility': 10000, 
    }
    event_data = EventData(json_data)
    assert event_data.calc_golden_score() == 66

def test_event_score_temp_low_good():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 65}, 
        'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 
        'visibility': 10000, 
    }
    event_data = EventData(json_data)
    assert event_data.calc_golden_score() == 100

def test_event_score_temp_high_good():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 75}, 
        'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 
        'visibility': 10000, 
    }
    event_data = EventData(json_data)
    assert event_data.calc_golden_score() == 100

def test_event_score_temp_low_mid():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 52.5}, 
        'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 
        'visibility': 10000, 
    }
    event_data = EventData(json_data)
    assert event_data.calc_golden_score() == 83

def test_event_score_temp_low_min():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 40}, 
        'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 
        'visibility': 10000, 
    }
    event_data = EventData(json_data)
    assert event_data.calc_golden_score() == 66

def test_event_score_temp_high_mid():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 87.5}, 
        'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 
        'visibility': 10000, 
    }
    event_data = EventData(json_data)
    assert event_data.calc_golden_score() == 83

def test_event_score_temp_high_min():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 100}, 
        'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 
        'visibility': 10000, 
    }
    event_data = EventData(json_data)
    assert event_data.calc_golden_score() == 66

def test_event_score_visibility_low_mid():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 
        'visibility': 2500, 
    }
    event_data = EventData(json_data)
    assert event_data.calc_golden_score() == 83

def test_event_score_visibility_low_min():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.calc_golden_score() == 66

def test_event_image_thunderstorm():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 200, 'main': 'Thunderstorm', 'description': 'light intensity drizzle', 'icon': '09d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.get_image_name() == "thunderstorm"

def test_event_image_drizzle():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 300, 'main': 'Drizzle', 'description': 'light intensity drizzle', 'icon': '09d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.get_image_name() == "drizzle"

def test_event_image_light_rain():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.get_image_name() == "light-rain"

def test_event_image_extreme_rain():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 504, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.get_image_name() == "extreme-rain"

def test_event_image_sleet():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 511, 'main': 'Snow', 'description': 'freezing rain', 'icon': '13d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.get_image_name() == "sleet"

def test_event_image_rain():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 501, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.get_image_name() == "rain"

def test_event_image_sleet_611():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 611, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.get_image_name() == "sleet"

def test_event_image_snow():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 600, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.get_image_name() == "snow"

def test_event_image_night():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 1800, 'main': 'Clear Night', 'description': 'light rain', 'icon': '10d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.get_image_name() == "clear-night"

def test_event_image_night_partial_cloud():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 1801, 'main': 'Clear Night', 'description': 'light rain', 'icon': '10d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.get_image_name() == "partly-cloudy-night"

def test_event_image_night_cloudy():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 1804, 'main': 'Clear Night', 'description': 'light rain', 'icon': '10d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.get_image_name() == "cloudy"

def test_event_image_fog():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 700, 'main': 'Mist', 'description': 'light rain', 'icon': '10d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.get_image_name() == "fog"

def test_event_image_unk():
    json_data = {
        'dt': 1762948800, 
        'main': {'temp': 70}, 
        'weather': [{'id': 54600, 'main': 'Mist', 'description': 'light rain', 'icon': '10d'}], 
        'visibility': 0, 
    }
    event_data = EventData(json_data)
    assert event_data.get_image_name() == "unknown"