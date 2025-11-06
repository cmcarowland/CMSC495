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
