'''
Golden Hour App Group 1
UMGC CMSC 495 7385
Shivam Patel, Raymond Rowland, Mariam Ahmed, Katrina Wilhelm, Paul Cooper
November 5, 2025

user.py

Defines the User Class representing application users
Provides methods to serialize and deserialize user data, and remove favorite locations.
'''

from flask_app.location import Location

class User:
    """
    Class representing a user in the application.
    """
    
    def __init__(self, email, username, password_hash, id=-1):
        """
        Initialize a new User instance.
        Args:
            email (str): The user's email address.
            username (str): The user's username.
            password_hash (str): The hashed password for the user.
        """
        self.id = id
        self.email = email
        self.user_name = username
        self.password_hash = password_hash
        self.favorite_locations = []
        self.last_login = ''

    def to_json(self):
        """
        Convert the User instance to a JSON-serializable dictionary.
        Returns:
            dict: A dictionary representation of the User instance.
        """

        return {
            'email': self.email,
            'username': self.user_name,
            'id': self.id,
            'password_hash': self.password_hash,
            'favorite_locations': [loc.to_json() for loc in self.favorite_locations]
        }

    def is_location_favorited(self, latitude, longitude) -> Location | None:
        """
        Check if a location is in the user's favorite locations.
        Args:
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.
        Returns:
            Location : The location found in favorites
        """

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return None

        for loc in self.favorite_locations:
            if loc.latitude == latitude and loc.longitude == longitude:
                return loc
            
        return None
    
    def add_favorite_location(self, location) -> bool:
        """
        Add a favorite location to the user's list.
        Args:
            location (Location): The Location instance to add.
        Returns:
            bool: True if the location was added, False if it was already in favorites.
        """
        
        loc = self.is_location_favorited(location.latitude, location.longitude)
        if loc is not None:
            return False
            
        self.favorite_locations.append(location)
        return True
    
    def remove_favorite_location(self, latitude, longitude) -> bool:
        """
        Remove a favorite location by latitude and longitude.
        Args:
            latitude (float): The latitude of the location to remove.
            longitude (float): The longitude of the location to remove.
        Returns:
            bool: True if the location was found and removed, False otherwise.
        """

        loc = self.is_location_favorited(latitude, longitude)
        if loc:
            self.favorite_locations.remove(loc)
            return True
        
        return False
    
    @staticmethod
    def from_json(data):
        """
        Create a User instance from a JSON dictionary.
        Args:
            data (dict): A dictionary containing user data.
        Returns:
            User: An instance of the User class.
        """

        user = User(data['email'], data['username'], data['password_hash'], data.get('id', -1))
        user.favorite_locations = [Location.from_json(loc) for loc in data.get('favorite_locations', [])]
        return user