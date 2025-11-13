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
from flask import Flask, render_template, request, redirect, url_for, flash, make_response

from dotenv import load_dotenv
from datetime import datetime, timezone
import base64
import os
import json
import random

def create_app():
    users_instance = Users()
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.environ.get("OPEN_WEATHER_MAP_API_KEY")

    def cookie() -> str:
        s = ""
        for _ in range(10):
            s = s + chr(random.randint(0x41, 0x67))

        return s

    def is_authed(req) -> bool:
        if 'auth' in req.cookies:
            if req.cookies['auth'] in users_instance.authenticated:
                return True

        return False

    @app.route('/')
    def index():
        # renders templates/index.html
        return render_template('index.html')

    def query_hourly_forecast(latitude, longitude):
        '''
        Queries the API for hourly weather data.
        '''

        weather_data = api.query_hourly_forecast(latitude, longitude)
        if weather_data is None:
            flash('Location not found. Please try again.', 'error')
            return redirect(url_for('index'))

        return render_template('cityData.html', weather_data=weather_data)

    @app.route('/submitCoord', methods=['POST'])
    def submit_coord():
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')

        if not longitude or not latitude:
            flash('Please provide both latitude and longitude.', 'error')
            return redirect( url_for('index'))
        
        return query_hourly_forecast(latitude, longitude)

    @app.route('/submitCity', methods=['POST'])
    def submit_city():
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')

        if not city and not state and not country:
            flash('Please provide a city, state (US), and country.', 'error')
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
        
        longitude = data[0]['lon']
        latitude = data[0]['lat']
        
        return query_hourly_forecast(latitude, longitude)

    @app.route('/login', methods=['POST'])
    def login():
        auth = request.data.decode('utf-8')
        data = json.loads(auth)        
        user_name, pw_hash = base64.b64decode(data['auth']).decode('utf-8').split(':')

        if users_instance.login(user_name=user_name, pw=pw_hash):
            c = cookie()
            resp = make_response(redirect(url_for('index')), 200)
            resp.set_cookie('auth', c)
            user = users_instance.get_user(user_name)
            if user:
                user.last_login = str(datetime.now(timezone.utc))
                users_instance.authenticated[c] = user
                return resp
            else:
                flash('Login failed. User not found.', 'error')
                return redirect(url_for('index'), code=401)
            
        else:
            flash('Login failed. Please check your username and password.', 'error')
            return redirect(url_for('index'), code=401)
        
    @app.route('/logout', methods=['POST'])
    def logout():
        user = None
        auth_cookie = request.cookies.get('auth')
        if auth_cookie and auth_cookie in users_instance.authenticated:
            user = users_instance.authenticated[auth_cookie]
            del users_instance.authenticated[auth_cookie]

        if user:
            user.last_login = ''
            resp = make_response(redirect(url_for('index')), 200)
            resp.delete_cookie('auth')
            return resp
        else:
            flash('Logout failed. User not found.', 'error')
            return redirect(url_for('index'), is_authed=False, code=401)
        
    return app


app_instance = create_app()