#ZTM Warsaw config
#todo add logging

raw_map_params = [
    {
        'place': 'Bielany,+Warszawa',
        'lat': '52.2969669',
        'lon': '20.90007'
     },
    {
        'place': 'Wola,+Warszawa',
        'lat': '52.2345959',
        'lon': '20.9229824'
    }
]

class ConfigureMaps:

    def __init__(self):
        self.source = 'https://www.google.com/maps/place/'
        self.zoom = '14z'
        self.params = '!5m1!1e1'

        self.urls = []
        self.places = []
        for elem in raw_map_params:
            self.urls.append(self.url_generator(
                elem.get('place'),
                elem.get('lat'),
                elem.get('lon')
            ))
            self.places.append(elem.get('place'))

    def url_generator(self, place, lat, lon):
        return f'{self.source}{place}/@{lat},{lon},{self.zoom}/data={self.params}'


