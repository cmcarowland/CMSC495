from flask import Flask, render_template, request
import api

app = Flask(__name__)

@app.route('/')
def index():
    # renders templates/index.html
    return render_template('index.html')

@app.route('/submitCoord', methods=['POST'])
def submit_coord():
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')

    if not longitude and not latitude:
        return render_template('index.html', error="Please provide both longitude and latitude.")

    weather_data = api.query_weather(latitude, longitude)
    if weather_data is None:
        return render_template('index.html', error="Location not found. Please try again.")
    
    return render_template('cityData.html', longitude=longitude, latitude=latitude, weather_data=weather_data)

@app.route('/submitCity', methods=['POST'])
def submit_city():
    city = request.form.get('city')
    state = request.form.get('state')
    country = request.form.get('country')

    if not city and not state and not country:
        return render_template('index.html', error="Please provide at least one of city, state, or country.")

    data = api.query_location(city, state, country)
    if data is None:
        return render_template('index.html', error="Location not found. Please try again.")
    
    longitude = data[0]['lon']
    latitude = data[0]['lat']
    
    weather_data = api.query_weather(latitude, longitude)
    if weather_data is None:
        return render_template('index.html', error="Weather data not found. Please try again.")
    
    return render_template('cityData.html', longitude=longitude, latitude=latitude, weather_data=weather_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
