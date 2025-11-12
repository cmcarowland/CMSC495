

class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.favorite_locations = []

    def to_json(self):
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            'favorite_locations': self.favorite_locations
        }