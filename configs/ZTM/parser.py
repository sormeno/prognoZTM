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
            json_data['Lines'],
            json_data['Brigade'],
            json_data['VehicleNumber'],
            None,
            json_data['Time'],
            None,
            json_data['Lat'],
            json_data['Lon']
        )


def pz2000actual_weather(json_data):
    try:
        wind_deg = json_data['wind']['deg'] if json_data['wind']['deg'] else None
    except Exception:
        wind_deg = None
        logger.debug(f'Could not extract wind deg value. Assigning None.')


    return (
        json_data['coord']['lat'],
        json_data['coord']['lon'],
        json_data['dt'],
        json_data['main']['temp'],
        json_data['main']['feels_like'],
        json_data['main']['pressure'],
        json_data['main']['humidity'],
        json_data['visibility'],
        json_data['wind']['speed'],
        wind_deg,
        json_data['clouds']['all'],
        json_data['sys']['sunrise'],
        json_data['sys']['sunset']
    )
