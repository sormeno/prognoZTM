import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='C:\\Users\\filip\\OneDrive\\Dokumenty\\Python Projects\\PrognoZTM\\logs.txt'
    )
logger = logging.getLogger('PrognoZTM')
logger.info('Started logging!')

import sys
import libs.lib_credentials.credentials as cred
import libs.lib_api.api_client as api
from libs.lib_database import db_clients, dbc
import importlib

# import libs.meteo as meteo
# import libs.weather as wthr
# import libs.dzem as dzem


kp = cred.PassDB(input('KDBX masterpass: '))

#Setup data sources and targets
transport_operator = 'ZTM' #also name of KeePass entry
weather_provider = 'OPEN_WEATHER'
tgt_database = 'MYSQL_DB' #also name of KeePass entry
tgt_transport_api_table = 'pz1000bus_tram'
tgt_weather_api_table = 'pz2000actual_weather'

#api params
raw_params = [
    [
        ['RESOURCE_ID_ATTR_NAME','f2e5503e927d-4ad3-9500-4ab9e55deb59'],
        ['VEHICLE_TYPE_ATTR_NAME','1']
    ],
    [
        ['RESOURCE_ID_ATTR_NAME', 'f2e5503e927d-4ad3-9500-4ab9e55deb59'],
        ['VEHICLE_TYPE_ATTR_NAME', '2']
    ]
]

#import configs
try:
    api_configs = importlib.import_module(f'configs.{transport_operator}')
    transport_api_config = api_configs.transport_api_config.ConfigureTransportAPI()
    weather_api_config = api_configs.weather_api_config.ConfigureWeatherAPI()

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

#Setup additional API params TODO make it independent on transport api config
try:
    transport_api_params = [
        [
            [transport_api_config.API_ATTRIBUTES['RESOURCE_ID_ATTR_NAME'], transport_api_config.RESOURCE_ID]
            ,[transport_api_config.API_ATTRIBUTES['VEHICLE_TYPE_ATTR_NAME'], '1' ]
        ],
        [
            [transport_api_config.API_ATTRIBUTES['RESOURCE_ID_ATTR_NAME'], transport_api_config.RESOURCE_ID]
            , [transport_api_config.API_ATTRIBUTES['VEHICLE_TYPE_ATTR_NAME'], '2']
        ]
    ]
except KeyError:
    logger.error(f'Key not found', exc_info=True)
    sys.exit()

#init clients objects
transport_api_client = api.LiveDataClient(kp, transport_operator, transport_api_config)
transport_api_table_client = db_clients.DatabaseObjectClient(kp, tgt_database, db_config, tgt_transport_table_config)
weather_api_client = api.LiveDataClient(kp, weather_provider, weather_api_config)
weather_api_table_client = db_clients.DatabaseObjectClient(kp, tgt_database, db_config, tgt_weather_table_config)

# program execution
for param in transport_api_params:
    transport_data = transport_api_client.get_data(param)[transport_api_config.JSON_RESULT_LABEL]
    transport_api_table_client.insert_json_bulk(transport_data)

weather_data=[]
for measure_point in weather_api_config.measure_points_coordinates:
    weather_data.append(weather_api_client.get_data(measure_point))
weather_api_table_client.insert_json_bulk(weather_data)

logger.info('Program finished!')