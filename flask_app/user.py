from flask_app.location import Location

class User:
    def __init__(self, email, username, password_hash):
        self.id = -1
        self.email = email
        self.user_name = username
        self.password_hash = password_hash
        self.favorite_locations = []
        self.last_login = ''

    def to_json(self):
        return {
            'email': self.email,
            'username': self.user_name,
            'password_hash': self.password_hash,
            'favorite_locations': [loc.to_json() for loc in self.favorite_locations]
        }
    
    def remove_favorite_location(self, latitude, longitude):
        for loc in self.favorite_locations:
            if loc.latitude == latitude and loc.longitude == longitude:
                self.favorite_locations.remove(loc)
                return True
        
        return False
    
    @staticmethod
    def from_json(data):
        user = User(data['email'], data['username'], data['password_hash'])
        user.favorite_locations = [Location.from_json(loc) for loc in data.get('favorite_locations', [])]
        return user