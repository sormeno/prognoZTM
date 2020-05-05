#tables
pz1000bus_tram = (
    "prognoztm_stage",
    "pz1000bus_tram",
    [
        'LINE',
        'BRIGADE',
        'VEHICLE_1',
        'VEHICLE_2',
        'DATE',
        'TIME',
        'LATITUDE',
        'LONGITUDE'
    ]
)

pz2000actual_weather = (
    "prognoztm_stage",
    "pz2000actual_weather",
    [
        'LATITUDE',
        'LONGITUDE',
        'DATETIME_UNIX',
        'TEMPERATURE_K',
        'WIND_CHILL_TEMP_K',
        'PRESSURE',
        'HUMIDITY',
        'VISIBILITY',
        'WIND_SPEED_MS',
        'WIND_DIRECTION_DEG',
        'CLOUDS_COVERAGE',
        'SUNRISE_UNIX',
        'SUNSET_UNIX'
    ]
)


pz3000traffic_data = (
    "prognoztm_stage",
    "pz3000traffic_data",
    [
        'TIMESTAMP',
        'LABEL',
        'COLOR',
        'COLOR_VALUES',
        'COUNT'
    ]
)