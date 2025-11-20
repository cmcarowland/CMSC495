#!/bin/bash

if [ -z "$1" ]; then
    echo -e "Error: No API key provided.\n"
    echo "Usage:"
    echo "source install.sh <API_KEY>"
    return
fi

echo "OPEN_WEATHER_MAP_API_KEY=$1" > .env
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r flask_app/requirements.txt
