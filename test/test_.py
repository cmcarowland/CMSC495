import pytest
from flask_app import api
from flask_app.golden_hour_data import EventData
from flask_app.app import create_app

@pytest.fixture
def app_fixture():
    appinst = create_app()
    appinst.config.update({
        "TESTING": True,
    })

    yield appinst

@pytest.fixture
def client_dummy(app_fixture):
    return app_fixture.test_client()
    
def test_app_creation(app_fixture):   
    assert app_fixture is not None

def test_appclient_creation(client_dummy):
    assert client_dummy is not None

def test_index_route(client_dummy):
    response = client_dummy.get('/')
    assert response.status_code == 200
    assert b'<title>GoldenHour</title>' in response.data

def test_city_data(client_dummy):
    response = client_dummy.post('/submitCity', data={
        'city': 'Los Angeles',
        'state': 'CA',
        'country': 'US'
    })
    assert response.status_code == 200
    assert b'Los Angeles, US' in response.data

def test_coord_data(client_dummy):
    response = client_dummy.post('/submitCoord', data={
        'latitude': '38.9',
        'longitude': '-77.1'
    })
    assert response.status_code == 200
    assert b'Arlington, US' in response.data


def test_no_location_information(client_dummy):
    response = client_dummy.post('/submitCity', data={
        'city': '',
        'state': '',
        'country': ''
    })
    assert response.status_code == 302
    assert b'<title>Redirecting...</title>' in response.data
    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Please provide a city, state (US), and country.' in msg for category, msg in flashed_messages if category == 'error')

def test_no_city_information(client_dummy):
    response = client_dummy.post('/submitCity', data={
        'city': '',
        'state': 'CA',
        'country': 'US'
    })
    assert response.status_code == 302
    assert b'<title>Redirecting...</title>' in response.data
    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Please provide a valid city.' in msg for category, msg in flashed_messages if category == 'error')

def test_no_state_information(client_dummy):
    response = client_dummy.post('/submitCity', data={
        'city': 'Los Angeles',
        'state': '',
        'country': 'US'
    })
    assert response.status_code == 302
    assert b'<title>Redirecting...</title>' in response.data
    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Please provide a state for US locations.' in msg for category, msg in flashed_messages if category == 'error')

def test_no_country_information_with_city_and_state(client_dummy):
    response = client_dummy.post('/submitCity', data={
        'city': 'Los Angeles',
        'state': 'CA',
        'country': ''
    })
    assert response.status_code == 200
    assert b'<title>Redirecting...</title>' not in response.data
    assert b'Los Angeles, US' in response.data

def test_no_country_outside_us(client_dummy):
    response = client_dummy.post('/submitCity', data={
        'city': 'Skopje',
        'state': '',
        'country': ''
    })
    assert response.status_code == 302
    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Please provide a country.' in msg for category, msg in flashed_messages if category == 'error')

def test_outside_us(client_dummy):
    response = client_dummy.post('/submitCity', data={
        'city': 'Skopje',
        'state': '',
        'country': 'MK'
    })
    assert response.status_code == 200
    assert b'Skopje, MK' in response.data

def test_no_coordinates_information(client_dummy):
    response = client_dummy.post('/submitCoord', data={
        'latitude': '',
        'longitude': ''
    })
    assert response.status_code == 302
    assert b'<title>Redirecting...</title>' in response.data
    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Please provide both latitude and longitude.' in msg for category, msg in flashed_messages if category == 'error')

def test_no_longitude_information(client_dummy):
    response = client_dummy.post('/submitCoord', data={
        'latitude': '38.9',
        'longitude': ''
    })
    assert response.status_code == 302
    assert b'<title>Redirecting...</title>' in response.data
    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Please provide both latitude and longitude.' in msg for category, msg in flashed_messages if category == 'error')

def test_no_latitude_information(client_dummy):
    response = client_dummy.post('/submitCoord', data={
        'latitude': '',
        'longitude': '-77'
    })
    assert response.status_code == 302
    assert b'<title>Redirecting...</title>' in response.data
    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Please provide both latitude and longitude.' in msg for category, msg in flashed_messages if category == 'error')


def test_invalid_location(client_dummy):
    response = client_dummy.post('/submitCity', data={
        'city': 'ThisCityDoesNotExist',
        'state': 'ZZ',
        'country': 'US'
    })
    assert response.status_code == 302
    assert b'<title>Redirecting...</title>' in response.data
    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Location not found. Please try again.' in msg for category, msg in flashed_messages if category == 'error')

def test_null_city_with_nonus_country(client_dummy):
    response = client_dummy.post('/submitCity', data={
        'city': '',
        'state': '',
        'country': 'GB'
    })
    assert response.status_code == 302
    assert b'<title>Redirecting...</title>' in response.data
    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Please provide a valid city.' in msg for category, msg in flashed_messages if category == 'error')

def test_bad_latitude_information(client_dummy):
    response = client_dummy.post('/submitCoord', data={
        'latitude': '625',
        'longitude': '-77'
    })
    assert response.status_code == 302
    assert b'<title>Redirecting...</title>' in response.data
    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Location not found. Please try again.' in msg for category, msg in flashed_messages if category == 'error')

def test_current_weather():
    response = api.query_current_weather(latitude='38.9', longitude='-77.1')
    assert response is not None

def test_current_weather_bad_data():
    response = api.query_current_weather(latitude='625', longitude='-77.1')
    assert response is None

def test_reverse_geocoding():
    response = api.get_city_name(latitude='38.9', longitude='-77.1')
    assert response == 'Arlington'

def test_reverse_geocoding_bad_data():
    response = api.get_city_name(latitude='625', longitude='-77.1')
    assert response is None

def test_location_query_bad_data():
    response = api.query_location(city='ThisCityDoesNotExist', state='ZZ', country='US')
    assert response is None

def test_location_query_bad_query():
    response = api.query_location(city='ThisCity,NoDataType=NotExist', state='ZZ', country='US')
    assert response is None

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