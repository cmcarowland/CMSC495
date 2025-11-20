'''
Golden Hour App Group 1
UMGC CMSC 495 7385
Shivam Patel, Raymond Rowland, Mariam Ahmed, Katrina Wilhelm, Paul Cooper
November 5, 2025

app.py

Handles Flask application routes and rendering templates.
/submitCoord and /submitCity routes process user input and fetch weather data.
'''

from flask_app.users import Users
from flask_app import api
from flask_app.location import Location
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, make_response

from dotenv import load_dotenv
from datetime import datetime, timezone
import base64
import os
import json
import random

def create_app():
    """
    Create and configure the Flask application.
    """
    users_instance = Users()
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.environ.get("OPEN_WEATHER_MAP_API_KEY")

    def cookie() -> str:
        """
        Generate a random cookie string.
        Returns:
            str: A random string to be used as a cookie value.
        """

        s = ""
        for _ in range(10):
            s = s + chr(random.randint(0x41, 0x67))

        return s
    
    def get_auth_user_name(req) -> str:
        """
        Get the authenticated user's name from the request cookies.
        Args:
            req: The Flask request object.
        Returns:
            str: The authenticated user's name or an error message.
        """

        if 'auth' in req.cookies:
            if req.cookies['auth'] in users_instance.authenticated:
                return users_instance.authenticated[req.cookies['auth']].user_name

        return "Invalid Login Token"
    
    def get_auth_user_id(req) -> str:
        """
        Get the authenticated user's ID from the request cookies.
        Args:
            req: The Flask request object.
        Returns:
            str: The authenticated user's ID or an error message.
        """
        
        if 'auth' in req.cookies:
            if req.cookies['auth'] in users_instance.authenticated:
                return users_instance.authenticated[req.cookies['auth']].id

        return "Invalid Login Token"

    def get_auth_user(req):
        """
        Get the authenticated user object from the request cookies.
        Args:
            req: The Flask request object.
        Returns:
            User: The authenticated user object or None if not authenticated.
        """
        
        if 'auth' in req.cookies:
            if req.cookies['auth'] in users_instance.authenticated:
                return users_instance.authenticated[req.cookies['auth']]

        return None
    
    def is_location_favorited(user, latitude, longitude) -> bool:
        """
        Check if a location is in the user's favorite locations.
        Args:
            user (User): The user object.
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.
        Returns:
            bool: True if the location is favorited, False otherwise.
        """

        for loc in user.favorite_locations:
            if loc.latitude == latitude and loc.longitude == longitude:
                return True
            
        return False

    @app.route('/')
    def index():
        """
        Render the index page.
        Returns:
            The rendered index.html template.
        """

        user = get_auth_user(request)
        return render_template('index.html', user=user)

    def query_hourly_forecast(latitude, longitude, city_info=None):
        """
        Query the hourly forecast for given coordinates.
        Args:
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.
            city_info (dict, optional): City information dictionary. Defaults to None.
        Returns:
            The rendered cityData.html template with weather data or a redirect to index with an error message
        """

        weather_data = api.query_hourly_forecast(latitude, longitude)
        if weather_data is None:
            flash('Location not found. Please try again.', 'error')
            return redirect(url_for('index'))

        user = get_auth_user(request)
        if city_info is None:
            city_info = api.get_city_name(latitude, longitude)

        return render_template('cityData.html', weather_data=weather_data, user=user, city_info=city_info)

    @app.route('/submitCoord', methods=['POST'])
    def submit_coord():
        """
        Submit coordinates to get weather data.
        Args:
            Form data containing 'latitude' and 'longitude'.
        Returns:
            The rendered cityData.html template with weather data or a redirect to index with an error message.
        """

        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')

        if not longitude or not latitude:
            flash('Please provide both latitude and longitude.', 'error')
            return redirect( url_for('index'))
        
        return query_hourly_forecast(latitude, longitude, None)

    @app.route('/submitCity', methods=['POST'])
    def submit_city():
        """
        Submit city information to get weather data.
        Args:
            Form data containing 'city', 'state', and 'country'.
        Returns:
            The rendered cityData.html template with weather data or a redirect to index with an error message.
        """

        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')


        if not city and not state and not country:
            flash('Please provide a city, state (US), and country.', 'error')
            return redirect(url_for('index'))

        for input in [city, state, country]:
            if input and any(ch.isdigit() for ch in input):
                flash("Input fields cannot contain numbers.", 'error')
                return redirect(url_for('index'))
            
        if country in ['US', 'USA', 'United States', 'United States of America']:
            if not state:
                flash('Please provide a state for US locations.', 'error')
                return redirect(url_for('index'))
            elif not city:
                flash('Please provide a valid city.', 'error')
                return redirect(url_for('index'))
        elif not country:
            if city and state:
                country = 'US'
            else:
                flash('Please provide a country.', 'error')
                return redirect(url_for('index'))
        else:
            if not city:
                flash('Please provide a valid city.', 'error')
                return redirect(url_for('index'))

        data = api.query_location(city, state, country)
        if data is None:
            flash('Location not found. Please try again.', 'error')
            return redirect(url_for('index'))
        
        for location in data:
            if location['name'] == city:
                data = [location]
                break

        if len(data) > 1:
            return render_template('selectLocation.html', locations=data)
        
        longitude = data[0]['lon']
        latitude = data[0]['lat']
        
        return query_hourly_forecast(latitude, longitude, data[0])

    @app.route('/login', methods=['POST'])
    def login():
        """
        Login an existing user.
        Args:
            Form data containing 'auth' key with base64 encoded 'email:password_hash'.
        Returns:
            A redirect response to the index page with a success or error message.
        """

        auth = request.data.decode('utf-8')
        data = json.loads(auth)        
        email, pw_hash = base64.b64decode(data['auth']).decode('utf-8').split(':')

        user = users_instance.get_user(email)
        if user: 
            if users_instance.login(email, pw_hash):
                c = cookie()
                resp = make_response(redirect(url_for('index')), 200)
                resp.set_cookie('auth', c)
                user.last_login = str(datetime.now(timezone.utc))
                users_instance.authenticated[c] = user
                flash('Login successful.', 'success')
                return resp
            else:
                flash('Login failed. Please check your username and password.', 'error')
                return redirect(url_for('index'), code=401)
 
        else:
            flash('Login failed. User not found or invalid password.', 'error')
            return redirect(url_for('index'), code=401)
            
    @app.route('/signup', methods=['POST'])
    def signup():
        """
        Signup a new user.
        Args:
            Form data containing 'auth' key with base64 encoded 'email:username:password_hash'.
        Returns:
            A redirect response to the index page with a success or error message.
        """
        user = None
        auth = request.data.decode('utf-8')
        data = json.loads(auth)       
        email, user_name, pw_hash = base64.b64decode(data['auth']).decode('utf-8').split(':')
        user = users_instance.get_user(email)
        if user:
            flash('Signup failed. User already exists.', 'error')
            return redirect(url_for('index'), code=401)
        
        if users_instance.add_user(email, user_name, pw_hash):
            c = cookie()
            resp = make_response(redirect(url_for('index')), 200)
            resp.set_cookie('auth', c)
            user = users_instance.get_user(email)
            if user:
                user.last_login = str(datetime.now(timezone.utc))
                users_instance.authenticated[c] = user
                flash('Signup successful.', 'success')
                return resp
            else:
                flash('Signup failed. User not found.', 'error')
                return redirect(url_for('index'), code=401)
            
        else:
            flash('Signup failed. Please check your username and password.', 'error')
            return redirect(url_for('index'), code=401)
        
    @app.route('/logout', methods=['POST'])
    def logout():
        """
        Logout the current user.
        Returns:
            A redirect response to the index page with a success or error message.
        """

        user = None
        auth_cookie = request.cookies.get('auth')
        if auth_cookie and auth_cookie in users_instance.authenticated:
            user = users_instance.authenticated[auth_cookie]
            del users_instance.authenticated[auth_cookie]

        if user:
            user.last_login = ''
            flash('Logout successful.', 'success')
            resp = make_response(redirect(url_for('index')), 200)
            resp.delete_cookie('auth')
            return resp
        else:
            flash('Logout failed. User was not logged in.', 'error')
            user = users_instance.get_user_by_id(get_auth_user_id(request))
            if user:
                user.last_login = ''
            resp = make_response(redirect(url_for('index')), 200)
            resp.delete_cookie('auth')
            return resp
    
    @app.route('/city', methods=['GET'])
    def city():
        """
        Render the city weather data page based on query parameters.
        Returns:
            The rendered cityData.html template with weather data or a redirect to index with an error message.
        """

        lat = request.args.get('latitude')
        lon = request.args.get('longitude')
        if not lat or not lon:
            flash('Missing coordinates.', 'error')
            return redirect(url_for('index'))
        
        try:
            latf = float(lat)
            lonf = float(lon)
        except (TypeError, ValueError):
            flash('Invalid coordinates.', 'error')
            return redirect(url_for('index'))

        return query_hourly_forecast(latf, lonf)
    
    @app.route('/favorite', methods=['POST', 'OPTIONS'])
    def favorite():
        """
        Add a location to the user's favorites.
        Returns:
            A redirect response to the city page or index with an error message.
        """

        user = get_auth_user(request)
        if not user:
            flash('You must be logged in to favorite a location.', 'error')
            return redirect(url_for('index'))

        data = request.data.decode('utf-8')
        loc_data = json.loads(data)
        location = Location.from_json(loc_data)
        if is_location_favorited(user, location.latitude, location.longitude):
            if user.remove_favorite_location(location.latitude, location.longitude):
                users_instance.save()
                return jsonify({"action": 'removed'}), 200
            else:
                flash('Failed to remove favorite location.', 'error')
                return make_response('', 400)
        else:
            if user.add_favorite_location(location):
                users_instance.save()
                return jsonify({"action": 'added'}), 200
            else:
                flash('Failed to add favorite location.', 'error')
                return make_response('', 400)
    
    # Register global template functions so they can be used in Jinja2 templates
    app.jinja_env.globals['get_auth_user_name'] = get_auth_user_name
    app.jinja_env.globals['get_auth_user_id'] = get_auth_user_id
    app.jinja_env.globals['is_location_favorited'] = is_location_favorited
    return app


app_instance = create_app()