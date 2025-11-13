

class User:
    def __init__(self, username, password_hash):
        self.user_name = username
        self.password_hash = password_hash
        self.favorite_locations = []
        self.last_login = ''

    def to_json(self):
        return {
            'username': self.user_name,
            'password_hash': self.password_hash,
            'favorite_locations': self.favorite_locations
        }
    
    @staticmethod
    def from_json(data):
        user = User(data['username'], data['password_hash'])
        user.favorite_locations = data.get('favorite_locations', [])
        return user