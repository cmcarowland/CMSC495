'''
Golden Hour App Group 1
UMGC CMSC 495 7385
Shivam Patel, Raymond Rowland, Mariam Ahmed, Katrina Wilhelm, Paul Cooper
November 18, 2025

__main__.py

Entry point for the Flask application.
Used to run the app locally for development and testing.
'''

from .app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)