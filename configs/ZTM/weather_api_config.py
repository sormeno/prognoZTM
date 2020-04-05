#ZTM Warsaw config
import logging
import sys
logger = logging.getLogger('prognoZTM.weather_config')

class ConfigureWeatherAPI:
    def __init__(self):
        self.API_ATTRIBUTES ={
            #NECCESSARY ATTRIBUTE - DO NOT REMOVE
            'API_ATTR_NAME' : 'appid',

            #Optional attributes
            'LATITUDE_ATTR_NAME' : 'lat',
            'LONGITUDE_ATTR_NAME' : 'lon',
            'PLACE_NAME_ATTR_NAME' : 'q',
            'CITY_ID_ATTR_NAME' : 'id'
        }

        # NECCESSARY CONSTANTS - DO NOT REMOVE
        self.INVALID_API_KEY_CHECK = {
            'label':'cod',
            'result':'401'
        }

        self.lat_max = 52.38
        self.lat_min = 52.08
        self.lon_max = 21.25
        self.lon_min = 20.85

        self.measure_points_coordinates = self.get_weather_coordinates()
        # Optional constants
        #None

    def get_weather_coordinates(self):

        try:
            if (self.lat_max-self.lat_min > 1):
                logger.warning(f'Latitude range is {self.lat_max-self.lat_min} degrees. Consider smaller range.')
                print(f'Latitude range is {self.lat_max - self.lat_min} degrees. Consider smaller range.')
            if (self.lon_max-self.lon_min > 1):
                logger.warning(f'Latitude range is {self.lon_max-self.lon_min} degrees. Consider smaller range.')
                print(f'Latitude range is {self.lon_max-self.lon_min} degrees. Consider smaller range.')
        except Exception as e:
            logger.error(f'Provided weather coordinates extrema are not correct. Please correct them.', exc_info = True)
            print(f'Provided weather coordinates extrema are not correct. Please correct them.')
            sys.exit()


        lat = self.lat_min + 0.025
        lon = self.lon_min + 0.025

        logger.info(f'Starting generating weather coordinates with latitude = {lat} and longitude = {lon}.')
        measure_points_coordinates = []

        while lat < self.lat_max:
            while lon < self.lon_max:
                measure_points_coordinates.append([
                    [self.API_ATTRIBUTES['LATITUDE_ATTR_NAME'],lat],
                    [self.API_ATTRIBUTES['LONGITUDE_ATTR_NAME'],lon]
                ])
                logger.info(f'Weather coordinate: lat={lat};lon={lon} added to list.')
                lon += 0.05
            lat += 0.05

        return measure_points_coordinates



