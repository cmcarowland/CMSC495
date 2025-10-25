# Golden Hour Flask App

Minimal scaffold for the Golden Hour sunrise/sunset planner.

Quick start

1. Create and activate a virtualenv (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the server:

```bash
OPEN_WEATHER_MAP_API_KEY={APIKEY} python app.py
```

3. Open http://localhost:5000 in your browser.

Files
- `app.py` - minimal Flask server
- `templates/index.html` - base page (references `/static/resources/icon.svg`)
- `static/resources/Sunapp*.png` - app icons
- `static/css/style.css` - simple styles

Next steps
- [x] Wire up API endpoints for sunrise/sunset and weather
- [ ] Add unit tests and CI
