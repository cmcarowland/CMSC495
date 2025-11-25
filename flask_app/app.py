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
            return render_template('invalid_location.html', weather_data={"coordinates": (latitude, longitude)}), 204

        user = get_auth_user(request)
        if city_info is None:
            city_info = api.get_city_name(latitude, longitude)

        return render_template('weather_grid.html', weather_data=weather_data, city_info=city_info, user=user), 200
    
    def get_city_data_quip():
        """
        Get a random quip about city data.
        Returns:
            str: A random quip string.
        """

        sun_quips = [
            "Don’t worry, the sun's not the only thing that needs a warm-up. Data’s almost here!",
            "This sun's got nothing on the data we're about to hit you with. Patience, sunshine!",
            "Data loading faster than a sunbeam through a window. Well, almost... Hang tight!",
            "If you think the sunrise is slow? Please. This data’s got more style than that golden hour glow!",
            "You thought the sunrise was slow? Please.",
            "Sun’s almost up, and so is your weather info! Just don’t blink, you might miss it!",
            "Data’s like the sun, it’ll get here when it gets here—but when it does, it’ll light up your day!",
            "Patience, friend. The sun isn’t the only thing that rises slowly—just wait for this perfect weather report!",
            "I’d say this is as slow as waiting for a sunset, but who needs sunsets when you’ve got data like this?",
            "The sun might be slow to rise, but don’t worry, your weather data will shine soon enough!",
            "Like the sun’s first rays—data’s coming in hot. But for now, enjoy the anticipation!",
            "Think of this as the calm before the storm... of perfect weather data. Coming right up!",
            "Sunrise? Too slow. Data? A little faster—just hold on!",
            "You know what’s slower than a sunrise? This API… But don’t worry, we’re almost there!",
            "I promise, this data will shine brighter than the sun… but first, it’s gotta wake up!"
        ]

        return random.choice(sun_quips)

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
        
        return render_template('cityData.html', latitude=latitude, longitude=longitude, quip=get_city_data_quip())

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
            
        if country in ['US']:
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

        return render_template('cityData.html', city=city, state=state, country=country, quip=get_city_data_quip())

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
            users_instance.save()
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
            flash('You must be logged in to perform favorite actions.', 'error')
            return redirect(url_for('index'))

        data = request.data.decode('utf-8')
        loc_data = json.loads(data)
        location = Location.from_json(loc_data)
        if user.is_location_favorited(location.latitude, location.longitude):
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
            
    @app.route('/renderFavorites', methods=['GET'])
    def render_favorites():
        '''
        Render favorite locations list.
        Returns:
            JSON response with rendered HTML for favorite locations.
        '''

        user = get_auth_user(request)
        html = render_template("favoriteLocations.html", user=user)
        return jsonify({"html": html})
    
    def get_city_info(city, state, country):
        '''
        Get city information dictionary.
        Args:
            city (str): City name.
            state (str): State name.
            country (str): Country name.
        Returns:
            The rendered cityData.html template with weather data or a redirect to index with an error message.
        '''

        data = api.query_location(city, state, country)
        if data is None:
            # flash('Location not found. Please try again.', 'error')
            print("data is none!!!")
            return render_template('invalid_location.html', weather_data={}), 204
        
        for location in data:
            if location['name'] == city:
                data = [location]
                break

        if len(data) > 1:
            return render_template('selectLocation.html', locations=data), 201
        
        longitude = data[0]['lon']
        latitude = data[0]['lat']
        
        return query_hourly_forecast(latitude, longitude, data[0])

    @app.route('/getQuip', methods=['GET'])
    def getQuip():
        '''
        Render a random quip about city data.
        Returns:
            JSON response with the quip string.
        '''

        html = render_template("quip.html", quip=get_city_data_quip())
        return jsonify({"html": html})

    @app.route('/renderWeather', methods=['POST'])
    def renderWeather():
        '''
        Render weather data grid.
        Expects JSON data with 'weather_data' key.
        Returns:
            JSON response with rendered HTML for weather data grid.
        '''

        if request.json: 
            if 'latitude' in request.json and request.json['latitude']:
                html, status = query_hourly_forecast(request.json['latitude'], request.json['longitude'])
            elif 'city' in request.json and request.json['city']:
                html, status = get_city_info(request.json['city'], request.json.get('state'), request.json['country'])

        return jsonify({"html": html, "status": status})

    # Register global template functions so they can be used in Jinja2 templates
    app.jinja_env.globals['get_auth_user_name'] = get_auth_user_name
    app.jinja_env.globals['get_auth_user_id'] = get_auth_user_id
    return app


app_instance = create_app()