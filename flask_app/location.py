

class Location:
    def __init__(self, name, country, latitude, longitude, state = ''):
        self.name = name
        self.state = state
        self.country = country
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def from_json(data):
        name = data.get('name', '')
        state = data.get('state', '')
        country = data.get('country', '')
        latitude = data.get('lat', 0.0)
        longitude = data.get('lon', 0.0)
        return Location(name, country, latitude, longitude, state)
    
    def to_json(self):
        return {
            'name': self.name,
            'state': self.state,
            'country': self.country,
            'lat': self.latitude,
            'lon': self.longitude
        }