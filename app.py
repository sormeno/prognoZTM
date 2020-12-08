import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.INFO,
    filename='C:\\Users\\filip\\OneDrive\\Dokumenty\\Programowanie\\Python Projects\\PrognoZTM\\logs.txt'
    )
logger = logging.getLogger('PrognoZTM')
logger.info('Started logging!')

import time
import sys
from datetime import datetime
import importlib



################################# USER INPUT CONFIGS
#Setup data sources and targets
transport_operator = 'ZTM' #also alias for KeePass entry in KeePass_config.py
weather_provider = 'OPEN_WEATHER' #also alias for KeePass entry in KeePass_config.py
tgt_database = 'MYSQL_DB' #also alias for KeePass entry in KeePass_config.py
tgt_transport_api_table = 'pz1000bus_tram'
tgt_weather_api_table = 'pz2000actual_weather'
tgt_maps_table = 'pz3000traffic_data'

#Transport api params
transport_api_params = [
    [
        ['RESOURCE_ID_ATTR_NAME','f2e5503e927d-4ad3-9500-4ab9e55deb59'],
        ['VEHICLE_TYPE_ATTR_NAME','1']
    ],
    [
        ['RESOURCE_ID_ATTR_NAME', 'f2e5503e927d-4ad3-9500-4ab9e55deb59'],
        ['VEHICLE_TYPE_ATTR_NAME', '2']
    ]
]

################################# GENERATING CONFIGS
#import configs
try:
    import libs.lib_credentials.credentials as cred
    import libs.lib_api.api_client as api
    from libs.lib_database import db_clients, dbc
    from libs.lib_screenshots import screen_analyzer

    kp = cred.JSONpassDB()
    api_configs = importlib.import_module(f'configs.{transport_operator}')
    db_config = getattr(importlib.import_module(f'configs.databases.database_config'), f'{tgt_database}')

except Exception as e:
    logger.error(f'Initing configs failed with {e}', exc_info=True)
    print(f'Initing configs failed with {e}')
    sys.exit()


#transport data
def transport_data_get_continously():
    try:
        transport_api_config = api_configs.transport_api_config.ConfigureTransportAPI()

        tgt_transport_table_meta = getattr(importlib.import_module(f'configs.databases.tables_config'), f'{tgt_transport_api_table}')
        tgt_transport_table_parser = getattr(importlib.import_module(f'configs.{transport_operator}.parser'), f'{tgt_transport_api_table}')
        tgt_transport_table_config = dbc.TableInfo(*tgt_transport_table_meta, tgt_transport_table_parser)

    except Exception as e:
        logger.error(f'Initing configs failed with {e}', exc_info=True)
        print(f'Initing configs failed with {e}')
        sys.exit()

    transport_api_client = api.LiveDataClient(kp, transport_operator, transport_api_config)
    transport_api_table_client = db_clients.DatabaseObjectClient(kp, tgt_database, db_config, tgt_transport_table_config)

    for param in transport_api_params:
        start = time.time()
        transport_data = transport_api_client.get_data(param)[transport_api_config.JSON_RESULT_LABEL]
        logger.info(f'Getting transport data took {time.time() - start}')

        start = time.time()
        for elem in transport_data:
            transport_api_table_client.insert_json(elem)
        logger.info(f'Inserted {len(transport_data)} rows with transport data.Inserting took {time.time() - start}')


#weather data
def weather_data_get_continously():
    try:
        weather_api_config = api_configs.weather_api_config.ConfigureWeatherAPI()

        tgt_weather_table_meta = getattr(importlib.import_module(f'configs.databases.tables_config'), f'{tgt_weather_api_table}')
        tgt_weather_table_parser = getattr(importlib.import_module(f'configs.{transport_operator}.parser'), f'{tgt_weather_api_table}')
        tgt_weather_table_config = dbc.TableInfo(*tgt_weather_table_meta, tgt_weather_table_parser)

    except Exception as e:
        logger.error(f'Initing configs failed with {e}', exc_info=True)
        print(f'Initing configs failed with {e}')
        sys.exit()

    weather_api_client = api.LiveDataClient(kp, weather_provider, weather_api_config)
    weather_api_table_client = db_clients.DatabaseObjectClient(kp, tgt_database, db_config, tgt_weather_table_config)

    weather_data=[]
    start = time.time()
    for measure_point in weather_api_config.measure_points_coordinates:
        weather_data.append(weather_api_client.get_data(measure_point))
    logger.info(f'Getting weather data took {time.time() - start}')

    start = time.time()
    for elem in (weather_data):
        weather_api_table_client.insert_json(elem) #_bulk off #TODO fix bulk insert
    logger.info(f'Inserting weather data took {time.time() - start}')


#traffic
def traffic_data_get_continously():
    try:
        maps_config = api_configs.maps_config.ConfigureMaps()
        from configs.screenshots.selenium_config import selenium_config
        from configs.screenshots.screenshot_config import screen_analyzer_config

        tgt_maps_table_meta = getattr(importlib.import_module(f'configs.databases.tables_config'), f'{tgt_maps_table}')
        tgt_maps_table_parser = getattr(importlib.import_module(f'configs.{transport_operator}.parser'),
                                        f'{tgt_maps_table}')
        tgt_maps_table_config = dbc.TableInfo(*tgt_maps_table_meta, tgt_maps_table_parser)

    except Exception as e:
        logger.error(f'Initing configs failed with {e}', exc_info=True)
        print(f'Initing configs failed with {e}')
        sys.exit()

    maps_client = screen_analyzer.ScreenAnalyzer(selenium_config, screen_analyzer_config)
    maps_table_client = db_clients.DatabaseObjectClient(kp, tgt_database, db_config, tgt_maps_table_config)

    start = time.time()
    for elem, place in zip(maps_config.urls, maps_config.places):
        traffic_data = maps_client.get_screen(elem).get_image_pixels(place, datetime.now())
        maps_table_client.insert_json_bulk(traffic_data)
    logger.info(f'Gathering traffic data took {time.time() - start}')



if __name__ == "__main__":
    data_source = (sys.argv[1])
    {
        'transport': transport_data_get_continously,
        'weather': weather_data_get_continously,
        'traffic': traffic_data_get_continously
    }[data_source]()



logger.info('Program finished!')