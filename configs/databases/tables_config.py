#tables
pz1000bus_tram = (
    "baza22697_prognoztm_stage",
    "pz1000bus_tram",
    [
        'LINE',
        'BRIGADE',
        'VEHICLE',
        'DATE_API',
        'DATE_COLLECTED',
        'LATITUDE',
        'LONGITUDE'
    ]
)

pz2000actual_weather = (
    "baza22697_prognoztm_stage",
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
    "baza22697_prognoztm_stage",
    "pz3000traffic_data",
    [
        'TIMESTAMP',
        'LABEL',
        'COLOR',
        'COLOR_VALUES',
        'COUNT'
    ]
)