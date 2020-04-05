#ZTM Parsers
import logging

logger = logging.getLogger("PrognoZTM.ZTM_parser")

def pz1000bus_tram(json_data):
    try:
        if '+' in json_data['VehicleNumber']:
            vehicle_1,vehicle_2 = json_data['VehicleNumber'].split('+')
        else:
            vehicle_1 = json_data['VehicleNumber']
            vehicle_2 = None
        logger.debug(f'Values extracted from API fields: vehicle_1={vehicle_1} and vehicle_2={vehicle_2}')

        date, time = json_data['Time'].split(' ')
        date.replace('-','')
        logger.debug(f'Values extracted from API fields: date={date} and time={time}')

        return (
            int(json_data['Lines']),
            int(json_data['Brigade']),
            int(vehicle_1),
            int(vehicle_2) if vehicle_2 else None,
            int(date.replace('-','')),
            time,
            json_data['Lat'],
            json_data['Lon']
        )

    except ValueError:
        logger.warning(f'Parsing failed with error {ValueError}. Error message:', exc_info = True)
        return (
            json_data['Lines'],
            json_data['Brigade'],
            json_data['VehicleNumber'],
            None,
            json_data['Time'],
            None,
            json_data['Lat'],
            json_data['Lon']
        )