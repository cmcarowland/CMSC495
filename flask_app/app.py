from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    # renders templates/index.html
    return render_template('index.html')

@app.route('/submitCity', methods=['POST'])
def submit_city():
    city = request.form.get('city')
    state = request.form.get('state')
    country = request.form.get('country')

    if not city and not state and not country:
        return render_template('index.html', error="Please provide at least one of city, state, or country.")

    url = f'https://geocode.maps.co/search?'
    if city:
        url += f'city={city}&'
    if state:
        url += f'state={state}&'
    if country:
        url += f'country={country}&'

    url += f'api_key={os.environ.get("GEOCODE_API_KEY")}'
    response = requests.post(url)
    data = response.json()
    if data is None or len(data) == 0:
        return render_template('index.html', error="Location not found. Please try again.")
    
    longitude = data[0]['lon']
    latitude = data[0]['lat']
    return render_template('cityData.html', longitude=longitude, latitude=latitude)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
