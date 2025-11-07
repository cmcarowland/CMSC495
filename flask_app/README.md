# Golden Hour Flask App

Golden Hour sunrise/sunset planner flask application.

Quick start

- Project Environment 
    - Linux codespaces-5b9dc1 6.8.0-1030-azure #35~22.04.1-Ubuntu SMP  
    - x86_64 GNU/Linux 
    - Python 3.12.1 

- Project Structure 
    - CMSC 495/ 
        - flask_app/ : Contains source code for the flask web application 
            - static/ : Folder containing static assets such as CSS and images
            - templates/ : Contains HTML template files for index and cityData endpoints 
            - api.py : Wrapper for API related code 
            - app.py : Main module for the flask application. Contains entry point and routing information 
            - golden_hour_data.py : Contains GoldenHourData, Day, and EventData classes to parse and cache relevant sunrise, sunset, and whether data 

1. Create and activate a virtualenv (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r flask_app/requirements.txt
```
OR to use the install script
```bash
. install.sh
```

2. Run the server:

```bash
# This will create a .env file with our secret simplyifying testing and execution
echo "OPEN_WEATHER_MAP_API_KEY={APIKEY}" > .env
# This starts the flask server
python -m flask_app/app.py
```

3. Open http://localhost:5000 in your browser.
