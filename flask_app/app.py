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

    weather_data = api.query_current_weather(latitude, longitude)
    if weather_data is None:
        return render_template('index.html', error="Location not found. Please try again.")
    
    return render_template('cityData.html', 
                           longitude=longitude, latitude=latitude, 
                           weather_data=weather_data, 
                           image_name=f"resources/weather/{get_image_name(weather_data)}.png")

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
    
    weather_data = api.query_hourly_forecast(latitude, longitude)
    if weather_data is None:
        return render_template('index.html', error="Weather data not found. Please try again.")

    return render_template('cityData.html', weather_data=weather_data)

def get_image_name(weather_data):
    weather_id = weather_data['weather'][0]['id']
    # if (weather_data['dt'] < weather_data['sys']['sunrise'] or
    #     weather_data['dt'] > weather_data['sys']['sunset']):
    #     weather_id += 1000

    if weather_id - 200 < 100:
        return "thunderstorm"
    
    if weather_id - 300 < 100:
        return "drizzle"
    
    if weather_id == 500:
        return "light-rain"
    elif weather_id == 504:
        return "extreme-rain"
    elif weather_id == 511:
        return "sleet"
    elif weather_id - 500 < 100:
        return "rain"
    
    if 611 <= weather_id <= 613:
        return "sleet"
    elif weather_id - 600 < 100:
        return "snow"
    
    if weather_id - 700 < 100:
        return "fog"
    
    if weather_id == 800:
        return "clear-day"
    
    if 801 <= weather_id <= 803:
        return "partly-cloudy-day"
    elif weather_id - 800 < 100:
        return "cloudy"
    
    # night icons
    if weather_id == 1800:
        return "clear-night"
    if 1801 <= weather_id <= 1803:
        return "partly-cloudy-night"
    elif weather_id == 1804:
        return "cloudy"

    return "unknown"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
