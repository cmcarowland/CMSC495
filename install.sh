#!/bin/bash

python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r flask_app/requirements.txt
