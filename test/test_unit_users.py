from flask_app.user import User
from flask_app.location import Location
from flask_app.users import Users

import hashlib
import pytest
import shutil

location = Location("Los Angeles", "US", 34.0522, -118.2437, "California")

def create_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@pytest.fixture
def user_fixture():
    user = User("tester@example.com", "tester", create_password_hash("password"))
    
    yield user

@pytest.fixture
def user_manager_fixture():
    shutil.copy("test/data/users.json", "test/users.json")
    Users.FILENAME =  "test/users.json"
    users_manager = Users()
    
    yield users_manager

def test_create_user():
    user = User("tester@example.com", "tester", create_password_hash("password"))
    assert user is not None 
    assert type(user) is User

def test_user_to_json(user_fixture):
    user_json = user_fixture.to_json()
    assert user_json['email'] == "tester@example.com"
    assert user_json['username'] == "tester"

def test_from_json(user_fixture):
    user_json = user_fixture.to_json()
    new_user = User.from_json(user_json)
    assert new_user.email == user_fixture.email
    assert new_user.user_name == user_fixture.user_name

def test_add_favorite_location(user_fixture):
    added = user_fixture.add_favorite_location(location)
    assert added is True
    assert len(user_fixture.favorite_locations) == 1

def test_add_duplicate_favorite_location(user_fixture):
    user_fixture.add_favorite_location(location)
    added = user_fixture.add_favorite_location(location)
    assert added is False
    assert len(user_fixture.favorite_locations) == 1

def test_remove_favorite_location(user_fixture):
    user_fixture.add_favorite_location(location)
    removed = user_fixture.remove_favorite_location(location.latitude, location.longitude)
    assert removed is True
    assert len(user_fixture.favorite_locations) == 0
    
def test_remove_nonexistent_favorite_location(user_fixture):
    removed = user_fixture.remove_favorite_location(location.latitude, location.longitude)
    assert removed is False
    assert len(user_fixture.favorite_locations) == 0

def test_user_manager(user_manager_fixture):
    users_manager = user_manager_fixture
    assert users_manager is not None
    assert type(users_manager) is Users

def test_add_user(user_manager_fixture, user_fixture):
    users_manager = user_manager_fixture
    added = users_manager.add_user(user_fixture.email, user_fixture.user_name, user_fixture.password_hash)
    assert added is True
    retrieved_user = users_manager.get_user(user_fixture.email)
    assert retrieved_user.user_name == user_fixture.user_name

def test_add_duplicate_user(user_manager_fixture, user_fixture):
    users_manager = user_manager_fixture
    users_manager.add_user(user_fixture.email, user_fixture.user_name, user_fixture.password_hash)
    added = users_manager.add_user(user_fixture.email, user_fixture.user_name, user_fixture.password_hash)
    assert added is False

def test_login_success(user_manager_fixture, user_fixture):
    users_manager = user_manager_fixture
    users_manager.add_user(user_fixture.email, user_fixture.user_name, user_fixture.password_hash)
    login_success = users_manager.login(user_fixture.email, user_fixture.password_hash)
    assert login_success is True

def test_login_failure_wrong_password(user_manager_fixture, user_fixture):
    users_manager = user_manager_fixture
    users_manager.add_user(user_fixture.email, user_fixture.user_name, user_fixture.password_hash)
    login_success = users_manager.login(user_fixture.email, create_password_hash("wrongpassword"))
    assert login_success is False

def test_login_failure_nonexistent_user(user_manager_fixture):
    users_manager = user_manager_fixture
    login_success = users_manager.login("nonexistent@example.com", create_password_hash("password"))
    assert login_success is False

def test_get_user_by_id(user_manager_fixture, user_fixture):
    users_manager = user_manager_fixture
    users_manager.add_user(user_fixture.email, user_fixture.user_name, user_fixture.password_hash)
    retrieved_user = users_manager.get_user(user_fixture.email)
    user_by_id = users_manager.get_user_by_id(retrieved_user.id)
    assert user_by_id is not None
    assert user_by_id.email == user_fixture.email

def test_get_user_by_id_nonexistent(user_manager_fixture):
    users_manager = user_manager_fixture
    user_by_id = users_manager.get_user_by_id(9999)
    assert user_by_id is None

def test_save(user_manager_fixture):
    users_manager = user_manager_fixture
    try:
        users_manager.save()
    except Exception as e:
        assert False, f"Save method raised an exception: {e}"