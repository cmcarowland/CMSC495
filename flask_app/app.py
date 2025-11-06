'''
Golden Hour App Group 1
UMGC CMSC 495 7385
Shivam Patel, Raymond Rowland, Mariam Ahmed, Katrina Wilhelm, Paul Cooper
November 5, 2025

app.py

Handles Flask application routes and rendering templates.
/submitCoord and /submitCity routes process user input and fetch weather data.
'''

from flask_app import api
from flask import Flask, render_template, request, redirect, url_for, flash

from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.environ.get("OPEN_WEATHER_MAP_API_KEY")

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

    return app

app_instance = create_app()