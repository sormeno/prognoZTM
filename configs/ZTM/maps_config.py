#ZTM Warsaw config
import logging
logger = logging.getLogger('prognoZTM.collect_screenshot')

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
            logger.info(f'Building URL for {elem.get("place")} and coordinates lat={elem.get("lat")}, lon={elem.get("lon")}')
            self.urls.append(self.url_generator(
                elem.get('place'),
                elem.get('lat'),
                elem.get('lon')
            ))
            logger.info(f'Appending places list with {elem.get("place")}')
            self.places.append(elem.get('place'))

    def url_generator(self, place, lat, lon):
        logger.info(f'Following URL for map screenshot built: {self.source}{place}/@{lat},{lon},{self.zoom}/data={self.params}')
        return f'{self.source}{place}/@{lat},{lon},{self.zoom}/data={self.params}'


