#ZTM Parsers
import logging
from datetime import datetime

logger = logging.getLogger("PrognoZTM.ZTM_parser")

def pz1000bus_tram(json_data):
    return (
        json_data.get('Lines', None),
        json_data.get('Brigade', None),
        json_data.get('VehicleNumber', None),
        json_data.get('Time', None),
        datetime.now(),
        json_data.get('Lat', None),
        json_data.get('Lon', None)
    )



def pz2000actual_weather(json_data):
    return (
        json_data.get('coord', {}).get('lat', None),
        json_data.get('coord', {}).get('lon', None),
        json_data.get('dt', None),
        json_data.get('main', {}).get('temp', None),
        json_data.get('main', {}).get('feels_like', None),
        json_data.get('main', {}).get('pressure', None),
        json_data.get('main', {}).get('humidity', None),
        json_data.get('visibility', None),
        json_data.get('wind', {}).get('speed', None),
        json_data.get('wind', {}).get('deg', None),
        json_data.get('clouds', {}).get('all', None),
        json_data.get('sys', {}).get('sunrise', None),
        json_data.get('sys', {}).get('sunset', None)
    )


def pz3000traffic_data(json_data):
    return (
        json_data.get('timestamp', None),
        json_data.get('label', None),
        json_data.get('color', None),
        json_data.get('pix_values', None),
        json_data.get('count', None)
    )
