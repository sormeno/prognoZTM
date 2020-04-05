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

#import configs
try:
    api_configs = importlib.import_module(f'configs.{transport_operator}')
    transport_api_config = api_configs.transport_api_config.ConfigureTransportAPI()
    weather_api_config = api_configs.weather_api_config.ConfigureWeatherAPI()

    db_config = getattr(importlib.import_module(f'configs.databases.database_config'), f'{tgt_database}')
    tgt_transport_table_meta = getattr(importlib.import_module(f'configs.databases.tables_config'), f'{tgt_transport_api_table}')
    tgt_transport_table_parser = getattr(importlib.import_module(f'configs.{transport_operator}.parser') ,f'{tgt_transport_api_table}')
    tgt_transport_table_config = dbc.TableInfo(*tgt_transport_table_meta, tgt_transport_table_parser)
except Exception as e:
    logger.error(f'Initing configs failed with {e}', exc_info=True)
    print(f'Initing configs failed with {e}')
    sys.exit()

#Setup additional API params TODO make it independent on transport api config
try:
    transport_api_params = [
        [transport_api_config.API_ATTRIBUTES['RESOURCE_ID_ATTR_NAME'], transport_api_config.RESOURCE_ID],
        [transport_api_config.API_ATTRIBUTES['VEHICLE_TYPE_ATTR_NAME'], '1' ],
        [transport_api_config.API_ATTRIBUTES['LINE_ATTR_NAME'], '157']
    ]
except KeyError:
    logger.error(f'Key not found', exc_info=True)
    sys.exit()

#init clients objects
transport_api_client = api.LiveDataClient(kp, transport_operator, transport_api_config)
transport_api_table_client = db_clients.DatabaseObjectClient(kp, tgt_database, db_config, tgt_transport_table_config)
weather_api_client = api.LiveDataClient(kp, weather_provider, weather_api_config)
#weather_api_table_client = db_clients.DatabaseObjectClient(kp, tgt_database, db_config, tgt_weather_table_config)




# program execution

transport_data = transport_api_client.get_data(transport_api_params)[transport_api_config.JSON_RESULT_LABEL]

transport_data = [
{'Lines': '157', 'Lon': '20.988461', 'VehicleNumber': '9428+4577+2558', 'Time': '2020-04-05 22:09:08', 'Lat': 52.24118, 'Brigade': '3'},
{'Lines': '157', 'Lon': 'blad', 'VehicleNumber': '9430', 'Time': '2020-04-05 22:09:07', 'Lat': 52.266479, 'Brigade': '6'},
{'Lines': 'karp', 'Lon': 20.963348, 'VehicleNumber': '9431', 'Time': '2020-04-05 22:09:07', 'Lat': 52.208298, 'Brigade': '4'},
{'Lines': '157', 'Lon': 20.976681, 'VehicleNumber': '9455', 'Time': '01-APR-2020 22:09:05', 'Lat': 52.289845, 'Brigade': '2'}
]

print(transport_data)
transport_api_table_client.insert_json(transport_data)
for measure_point in weather_api_config.measure_points_coordinates:
    weather_data = weather_api_client.get_data(measure_point)
#weather_api_table_client.insert_json(transport_data)

logger.info('Program finished!')