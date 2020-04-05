#ZTM Warsaw config
class ConfigureTransportAPI:
    def __init__(self):
        self.API_ATTRIBUTES ={
            #NECCESSARY ATTRIBUTE - DO NOT REMOVE
            'API_ATTR_NAME' : 'apikey',

            #Optional attributes
            'RESOURCE_ID_ATTR_NAME' : 'resource_id',
            'VEHICLE_TYPE_ATTR_NAME' : 'type',
            'LINE_ATTR_NAME' : 'line',
            'BRIGADE_ATTR_NAME' : 'brigade'
        }

        # NECCESSARY CONSTANTS - DO NOT REMOVE
        self.JSON_RESULT_LABEL = 'result'
        self.INVALID_API_KEY_CHECK = {
            'label':'result',
            'result':'false'
        }

        # Optional constants
        self.RESOURCE_ID = 'f2e5503e927d-4ad3-9500-4ab9e55deb59'