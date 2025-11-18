'''
Golden Hour App Group 1
UMGC CMSC 495 7385
Shivam Patel, Raymond Rowland, Mariam Ahmed, Katrina Wilhelm, Paul Cooper
November 18, 2025

location.py

Defines the Location class representing geographical locations.
Provides methods to serialize and deserialize location data.
'''

class Location:
    def __init__(self, name, country, latitude, longitude, state = ''):
        """
        Initialize a Location object.
        Args:
            name (str): Name of the location (city).
            country (str): Country code of the location.
            latitude (float): Latitude coordinate.
            longitude (float): Longitude coordinate.
            state (str, optional): State code of the location. Defaults to ''.
        """
        self.name = name
        self.state = state
        self.country = country
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def from_json(data):
        """
        Create a Location object from a JSON dictionary.
        Args:
            data (dict): A dictionary containing location data.
        Returns:
            Location: A Location object initialized with the provided data.
        """

        name = data.get('name', '')
        state = data.get('state', '')
        country = data.get('country', '')
        latitude = data.get('lat', 0.0)
        longitude = data.get('lon', 0.0)
        return Location(name, country, latitude, longitude, state)
    
    def to_json(self):
        """
        Serialize the Location object to a JSON-compatible dictionary.
        Returns:
            dict: A dictionary representation of the Location object.
        """
        
        return {
            'name': self.name,
            'state': self.state,
            'country': self.country,
            'lat': self.latitude,
            'lon': self.longitude
        }