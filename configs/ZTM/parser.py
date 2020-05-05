#ZTM Parsers
import logging

logger = logging.getLogger("PrognoZTM.ZTM_parser")

def pz1000bus_tram(json_data):
    try:
        line = json_data['Lines'].replace('-','000').replace('L','99901').replace('Z','99902').replace('E','99903').replace('N','99904')
        if '+' in json_data['VehicleNumber']:
            vehicle_1,vehicle_2 = json_data['VehicleNumber'].split('+')
        else:
            vehicle_1 = json_data['VehicleNumber']
            vehicle_2 = None

        logger.debug(f'Values extracted from API fields: line={line}')
        logger.debug(f'Values extracted from API fields: vehicle_1={vehicle_1} and vehicle_2={vehicle_2}')

        date, time = json_data['Time'].split(' ')
        date.replace('-','')
        logger.debug(f'Values extracted from API fields: date={date} and time={time}')

        return (
            int(line),
            int(json_data['Brigade']),
            int(vehicle_1),
            int(vehicle_2) if vehicle_2 else None,
            int(date.replace('-','')),
            time,
            json_data['Lat'],
            json_data['Lon']
        )

    except Exception as e:
        logger.warning(f'Parsing failed with error {e}. Error message:', exc_info = True)
        return (
            json_data.get('Lines', None),
            json_data.get('Brigade', None),
            json_data.get('VehicleNumber', None),
            None,
            json_data.get('Time', None),
            None,
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
