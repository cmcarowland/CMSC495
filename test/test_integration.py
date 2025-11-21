'''
Golden Hour App Group 1
UMGC CMSC 495 7385
Shivam Patel, Raymond Rowland, Mariam Ahmed, Katrina Wilhelm, Paul Cooper
November 21, 2025

test_integration.py

Integration tests for the Flask application.
Tests various routes and functionalities of the app.'''

import shutil
from flask_app import api
from flask_app.golden_hour_data import EventData
from flask_app.app import create_app
from flask_app.users import Users

import pytest
import hashlib
import base64
import shutil

@pytest.fixture
def app_fixture():
    shutil.copy("test/data/users.json", "test/users.json")
    Users.FILENAME =  "test/users.json"
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
    assert b'Los Angeles, California, US' in response.data

def test_coord_data(client_dummy):
    response = client_dummy.post('/submitCoord', data={
        'latitude': '38.9',
        'longitude': '-77.1'
    })
    assert response.status_code == 200
    assert b'Arlington, Virginia, US' in response.data


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
    assert b'Los Angeles, California, US' in response.data

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
    assert b'Skopje, Skopje Region, MK' in response.data

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
    assert response['name'] == 'Arlington'

def test_reverse_geocoding_bad_data():
    response = api.get_city_name(latitude='625', longitude='-77.1')
    assert response is None

def test_location_query_bad_data():
    response = api.query_location(city='ThisCityDoesNotExist', state='ZZ', country='US')
    assert response is None

def test_location_query_bad_query():
    response = api.query_location(city='ThisCity,NoDataType=NotExist', state='ZZ', country='US')
    assert response is None

def create_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def test_login_no_account(client_dummy):
    response = client_dummy.post('/login', json={
        'auth': base64.b64encode(f'tester@example.com:{create_password_hash("Tester123")}'.encode()).decode(),
    })

    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Login failed.' in msg for category, msg in flashed_messages if category == 'error')

def test_signup(client_dummy):
    response = client_dummy.post('/signup', json={
        'auth': base64.b64encode(f'tester@example.com:Tester:{create_password_hash("Tester123")}'.encode()).decode()
    })

    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Signup successful.' in msg for category, msg in flashed_messages if category == 'success')

def test_login_existing_account(client_dummy):
    response = client_dummy.post('/signup', json={
        'auth': base64.b64encode(f'tester2@example.com:Tester:{create_password_hash("Tester123")}'.encode()).decode()
    })

    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Signup failed.' in msg for category, msg in flashed_messages if category == 'error')

def test_login_successful_account(client_dummy):
    response = client_dummy.post('/login', json={
        'auth': base64.b64encode(f'tester2@example.com:{create_password_hash("Tester123")}'.encode()).decode()
    })

    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Login successful.' in msg for category, msg in flashed_messages if category == 'success')

def test_login_wrong_password(client_dummy):
    response = client_dummy.post('/login', json={
        'auth': base64.b64encode(f'tester2@example.com:{create_password_hash("WrongPassword")}'.encode()).decode()
    })

    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Login failed.' in msg for category, msg in flashed_messages if category == 'error')

def test_logout_successful_account(client_dummy):
    response = client_dummy.post('/login', json={
        'auth': base64.b64encode(f'tester2@example.com:{create_password_hash("Tester123")}'.encode()).decode()
    })

    response = client_dummy.post('/logout')
    assert response.status_code == 200

def test_logout_without_login(client_dummy):
        response = client_dummy.post('/logout')
        with client_dummy.session_transaction() as session:
            flashed_messages = session['_flashes']
            assert any('Logout failed.' in msg for category, msg in flashed_messages if category == 'error')

def test_query_city(client_dummy):
    response = client_dummy.get('/city',
        query_string={'latitude': '38.9', 'longitude': '-77.1'}
    )

    assert response.status_code == 200
    assert b'Arlington, Virginia, US' in response.data

def test_query_city_bad_lat(client_dummy):
    response = client_dummy.get('/city',
        query_string={'latitude': 'ASDF', 'longitude': '-77.1'}
    )

    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Invalid coordinates' in msg for category, msg in flashed_messages if category == 'error')

def test_query_city_bad_lon(client_dummy):
    response = client_dummy.get('/city',
        query_string={'latitude': '38.9', 'longitude': 'ASDF'}
    )

    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Invalid coordinates' in msg for category, msg in flashed_messages if category == 'error')

def test_query_city_missing_lat(client_dummy):
    response = client_dummy.get('/city',
        query_string={'longitude': '-77.1'}
    )

    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Missing coordinates' in msg for category, msg in flashed_messages if category == 'error')

def test_query_city_missing_lon(client_dummy):
    response = client_dummy.get('/city',
        query_string={'latitude': '38.9'}
    )

    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('Missing coordinates' in msg for category, msg in flashed_messages if category == 'error')

def test_unauth_favorite_location_add(client_dummy):
    response = client_dummy.post('/favorite', json={
        'lat': 38.9,
        'lon': -77.1,
        'name': 'Arlington',
        'state': 'VA',
        'country': 'US'
    })

    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('You must be logged in to perform favorite actions.' in msg for category, msg in flashed_messages if category == 'error')

def test_unauth_favorite_location_remove(client_dummy):
    response = client_dummy.post('/favorite', json={
        'lat': 38.9,
        'lon': -77.1
    })

    with client_dummy.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any('You must be logged in to perform favorite actions' in msg for category, msg in flashed_messages if category == 'error')

def test_favorite_location_remove(client_dummy):
    response = client_dummy.post('/login', json={
        'auth': base64.b64encode(f'tester2@example.com:{create_password_hash("Tester123")}'.encode()).decode()
    })

    response = client_dummy.post('/favorite', json={
        'lat': 33.4504,
        'lon': -82.1982,
    })

    assert response.json['action'] == 'removed'

def test_favorite_location_add(client_dummy):
    response = client_dummy.post('/login', json={
        'auth': base64.b64encode(f'tester2@example.com:{create_password_hash("Tester123")}'.encode()).decode()
    })

    response = client_dummy.post('/favorite', json={
        'lat': '38.62684098373759',
        'lon': '-90.19761349442946',
        'name': 'St. Louis',
        'state': 'MO',
        'country': 'US'
    })

    assert response.status_code == 200
    assert response.json['action'] == 'added'