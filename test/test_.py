import pytest
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