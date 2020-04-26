import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.INFO,
    filename='C:\\Users\\filip\\OneDrive\\Dokumenty\\Python Projects\\PrognoZTM\\logs.txt'
    )
logger = logging.getLogger('PrognoZTM')
logger.info('Started logging!')

import time
import sys
import libs.lib_credentials.credentials as cred
import libs.lib_api.api_client as api
from libs.lib_database import db_clients, dbc
from libs.lib_screenshots import screen_analyzer

import importlib

# import libs.meteo as meteo
# import libs.dzem as dzem

start = time.time()
kp = cred.PassDB(input('KDBX masterpass: '))
logger.info(f'Opening pass database took {time.time() - start}')
################################# USER INPUT CONFIGS
#Setup data sources and targets
transport_operator = 'ZTM' #also name of KeePass entry
weather_provider = 'OPEN_WEATHER'
tgt_database = 'MYSQL_DB' #also name of KeePass entry
tgt_transport_api_table = 'pz1000bus_tram'
tgt_weather_api_table = 'pz2000actual_weather'

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
    api_configs = importlib.import_module(f'configs.{transport_operator}')
    transport_api_config = api_configs.transport_api_config.ConfigureTransportAPI()
    weather_api_config = api_configs.weather_api_config.ConfigureWeatherAPI()
    maps_config = api_configs.maps_config.ConfigureMaps()  #todo create configure map class
    from configs.screenshots.selenium_config import selenium_config

    db_config = getattr(importlib.import_module(f'configs.databases.database_config'), f'{tgt_database}')
    tgt_transport_table_meta = getattr(importlib.import_module(f'configs.databases.tables_config'), f'{tgt_transport_api_table}')
    tgt_transport_table_parser = getattr(importlib.import_module(f'configs.{transport_operator}.parser') ,f'{tgt_transport_api_table}')
    tgt_transport_table_config = dbc.TableInfo(*tgt_transport_table_meta, tgt_transport_table_parser)

    tgt_weather_table_meta = getattr(importlib.import_module(f'configs.databases.tables_config'), f'{tgt_weather_api_table}')
    tgt_weather_table_parser = getattr(importlib.import_module(f'configs.{transport_operator}.parser') ,f'{tgt_weather_api_table}')
    tgt_weather_table_config = dbc.TableInfo(*tgt_weather_table_meta, tgt_weather_table_parser)

except Exception as e:
    logger.error(f'Initing configs failed with {e}', exc_info=True)
    print(f'Initing configs failed with {e}')
    sys.exit()

#init clients objects
transport_api_client = api.LiveDataClient(kp, transport_operator, transport_api_config)
transport_api_table_client = db_clients.DatabaseObjectClient(kp, tgt_database, db_config, tgt_transport_table_config)
weather_api_client = api.LiveDataClient(kp, weather_provider, weather_api_config)
weather_api_table_client = db_clients.DatabaseObjectClient(kp, tgt_database, db_config, tgt_weather_table_config)
maps_client = screen_analyzer.ScreenAnalyzer(selenium_config)
#maps_table_client

################################# PROGRAM EXECUTION
#transport data
for param in transport_api_params:
    start = time.time()
    transport_data = transport_api_client.get_data(param)[transport_api_config.JSON_RESULT_LABEL]
    logger.info(f'Getting transport data took {time.time() - start}')

    start = time.time()
    for elem in transport_data:
        transport_api_table_client.insert_json(elem)
    logger.info(f'Inserting transport data took {time.time() - start}')

#weather data
weather_data=[]
start = time.time()
for measure_point in weather_api_config.measure_points_coordinates:
    weather_data.append(weather_api_client.get_data(measure_point))
logger.info(f'Getting weather data took {time.time() - start}')

start = time.time()
weather_api_table_client.insert_json_bulk(weather_data)
logger.info(f'Inserting weather data took {time.time() - start}')

#dzem
#todo add logging
for elem in maps_config.urls:
    single_screen = maps_client.get_screen(elem)
    single_screen.show()


logger.info('Program finished!')